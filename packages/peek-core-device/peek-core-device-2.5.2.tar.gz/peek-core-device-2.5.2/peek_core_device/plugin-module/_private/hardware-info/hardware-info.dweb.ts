import {DeviceTypeEnum, HardwareInfoI} from "./hardware-info.abstract";
import {webUuid} from "./hardware-info.web";
import {TupleOfflineStorageService} from "@synerty/vortexjs";

export class HardwareInfo extends HardwareInfoI {
    constructor( private tupleStorage: TupleOfflineStorageService) {
        super();

    }

    uuid(): Promise<string> {
        return webUuid(this.tupleStorage);
    }

    description(): string {
        return navigator.userAgent;
    }


    deviceType(): DeviceTypeEnum {
        return DeviceTypeEnum.DESKTOP_WEB;
    }
}