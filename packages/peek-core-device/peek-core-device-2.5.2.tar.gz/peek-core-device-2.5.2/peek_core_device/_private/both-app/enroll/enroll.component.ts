import {Component, OnInit} from "@angular/core";
import { TitleService } from "@synerty/peek-plugin-base-js"
import { BalloonMsgService } from "@synerty/peek-plugin-base-js"
import {first} from "rxjs/operators";

import {
    ClientSettingsTuple,
    DeviceNavService,
    DeviceTupleService,
    EnrolDeviceAction
} from "@peek/peek_core_device/_private";

import {DeviceEnrolmentService, DeviceInfoTuple} from "@peek/peek_core_device";
import {DeviceTypeEnum} from "@peek/peek_core_device/_private/hardware-info/hardware-info.abstract";

import {ComponentLifecycleEventEmitter, TupleSelector} from "@synerty/vortexjs";


@Component({
    selector: 'core-device-enroll',
    templateUrl: 'enroll.component.web.html',
    moduleId: module.id
})
export class EnrollComponent extends ComponentLifecycleEventEmitter implements OnInit {

    data: EnrolDeviceAction = new EnrolDeviceAction();

    deviceType: DeviceTypeEnum;

    constructor(private balloonMsg: BalloonMsgService,
                private titleService: TitleService,
                private tupleService: DeviceTupleService,
                private nav: DeviceNavService,
                private enrolmentService: DeviceEnrolmentService) {
        super();

        this.deviceType = this.tupleService.hardwareInfo.deviceType();

        // Make sure we're not on this page when things are fine.
        let sub = this.doCheckEvent
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => {
                if (this.enrolmentService.isEnrolled()) {
                    this.nav.toHome();
                    sub.unsubscribe();
                } else if (this.enrolmentService.isSetup()) {
                    this.nav.toEnrolling();
                    sub.unsubscribe();
                }
            });


    }

    ngOnInit() {
        this.titleService.setEnabled(false);
        this.titleService.setTitle('');

        let t = this.deviceType;

        // Use DeviceInfoTuple to convert it.
        let deviceInfo = new DeviceInfoTuple();
        deviceInfo.setDeviceType(t);
        this.data.deviceType = deviceInfo.deviceType;

        this.tupleService.hardwareInfo.uuid()
            .then(uuid => {
                this.data.deviceId = uuid;
                this.checkForEnrollEnabled();
            });

    }

    private checkForEnrollEnabled(): void {
        let ts = new TupleSelector(ClientSettingsTuple.tupleName, {});
        this.tupleService.offlineObserver
            .subscribeToTupleSelector(ts)
            .pipe(first())
            .takeUntil(this.onDestroyEvent)
            .subscribe((settings: ClientSettingsTuple[]) => {
                if (settings.length != 1)
                    return;

                let setting: ClientSettingsTuple = settings[0];

                if (this.tupleService.hardwareInfo.isOffice()
                    && !setting.officeEnrollmentEnabled) {
                    this.autoEnroll();

                } else if (this.tupleService.hardwareInfo.isField()
                    && !setting.fieldEnrollmentEnabled) {
                    this.autoEnroll();
                }

            });
    }

    private autoEnroll(): void {
        this.data.description = this.data.deviceId;
        this.enrollClicked();
    }

    enrollEnabled(): boolean {
        if (this.data.description == null || !this.data.description.length)
            return false;

        return true;

    }

    enrollClicked() {
        if (!this.enrollEnabled()) {
            this.balloonMsg
                .showWarning("Please enter a unique description for this device");
            return;
        }

        this.tupleService.tupleAction.pushAction(this.data)
            .then((tuples: DeviceInfoTuple[]) => {
                this.balloonMsg.showSuccess("Enrollement successful");
            })
            .catch((err) => {
                this.balloonMsg.showError(err);
            });

    }


}
