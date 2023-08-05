import {Component, OnInit} from "@angular/core";
import { TitleService } from "@synerty/peek-plugin-base-js"
import {Observable} from "rxjs/Observable";

import {ComponentLifecycleEventEmitter} from "@synerty/vortexjs";

import {DeviceEnrolmentService} from "@peek/peek_core_device";

import {DeviceNavService, DeviceServerService} from "@peek/peek_core_device/_private";

@Component({
    selector: 'core-device-loading',
    templateUrl: 'loading.component.web.html',
    moduleId: module.id
})
export class LoadingComponent extends ComponentLifecycleEventEmitter implements OnInit {

    constructor(private titleService: TitleService) {
        super();

    }

    ngOnInit() {
        this.titleService.setEnabled(false);
        this.titleService.setTitle('');
    }

}
