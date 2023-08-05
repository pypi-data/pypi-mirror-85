import {Component, OnInit} from "@angular/core";
import { TitleService } from "@synerty/peek-plugin-base-js"
import { BalloonMsgService } from "@synerty/peek-plugin-base-js"

import {
    DeviceNavService,
    DeviceServerService,
    DeviceTupleService,
    EnrolDeviceAction,
    ServerInfoTuple
} from "@peek/peek_core_device/_private";

import {DeviceInfoTuple} from "@peek/peek_core_device";
import {DeviceTypeEnum} from "@peek/peek_core_device/_private/hardware-info/hardware-info.abstract";

import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";


@Component({
    selector: 'core-device-enroll',
    templateUrl: 'connect.component.web.html',
    moduleId: module.id
})
export class ConnectComponent extends ComponentLifecycleEventEmitter implements OnInit {

    server: ServerInfoTuple = new ServerInfoTuple();

    httpPortStr: string = '8000';
    websocketPortStr: string = '8001';

    deviceType: DeviceTypeEnum;
    isWeb: boolean;

    constructor(private balloonMsg: BalloonMsgService,
                private titleService: TitleService,
                private tupleService: DeviceTupleService,
                private nav: DeviceNavService,
                private deviceServerService: DeviceServerService) {
        super();


        this.deviceType = this.tupleService.hardwareInfo.deviceType();
        this.isWeb = this.tupleService.hardwareInfo.isWeb();

        this.deviceServerService.connInfoObserver
            .takeUntil(this.onDestroyEvent)
            .subscribe((info: ServerInfoTuple) => {
                this.server = info;
            });

        // Make sure we're not on this page when things are fine.
        let sub = this.doCheckEvent
            .takeUntil(this.onDestroyEvent)
            .subscribe(() => {
                if (this.deviceServerService.isConnected) {
                    this.nav.toEnroll();
                    sub.unsubscribe();
                } else if (this.deviceServerService.isSetup) {
                    this.nav.toConnecting();
                    sub.unsubscribe();
                }
            });

    }

    ngOnInit() {
        this.titleService.setEnabled(false);
        this.titleService.setTitle('');
    }


    connectEnabled(): boolean {

        if (this.server != null) {
            if (this.server.host == null || !this.server.host.length)
                return false;

            if (!parseInt(this.websocketPortStr))
                return false;

            if (!parseInt(this.httpPortStr))
                return false;

        }
        return true;
    }

    connectClicked() {
        try {
            this.server.httpPort = parseInt(this.httpPortStr);
            this.server.websocketPort = parseInt(this.websocketPortStr);

        } catch (e) {
            this.balloonMsg.showError("Port numbers must be integers.");
            return;
        }

        this.deviceServerService.setServer(this.server)
            .then(() => this.nav.toConnecting());

    }

    setUseSsl(val:boolean) {
        this.server.useSsl = val;
    }


}
