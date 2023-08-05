export enum DeviceTypeEnum {
    MOBILE_WEB,
    MOBILE_IOS,
    MOBILE_ANDROID,
    DESKTOP_WEB,
    DESKTOP_WINDOWS,
    DESKTOP_MACOS
}

export function isWeb(type: DeviceTypeEnum): boolean {
    return type == DeviceTypeEnum.MOBILE_WEB
        || type == DeviceTypeEnum.DESKTOP_WEB;
}

export function isField(type: DeviceTypeEnum): boolean {
    return type == DeviceTypeEnum.MOBILE_WEB
        || type == DeviceTypeEnum.MOBILE_ANDROID
        || type == DeviceTypeEnum.MOBILE_IOS;
}

export function isOffice(type: DeviceTypeEnum): boolean {
    return type == DeviceTypeEnum.DESKTOP_MACOS
        || type == DeviceTypeEnum.DESKTOP_WINDOWS
        || type == DeviceTypeEnum.DESKTOP_WEB;
}


export abstract class HardwareInfoI {
    abstract uuid(): Promise<string> ;

    abstract description(): string;

    abstract deviceType(): DeviceTypeEnum;

    isWeb(): boolean {
        return isWeb(this.deviceType());
    }

    isField(): boolean {
        return isField(this.deviceType());
    }

    isOffice(): boolean {
        return isOffice(this.deviceType());
    }
}
