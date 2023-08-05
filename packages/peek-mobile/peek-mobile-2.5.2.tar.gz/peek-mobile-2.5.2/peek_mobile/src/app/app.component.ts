import {Component} from "@angular/core";
import {VortexService, VortexStatusService} from "@synerty/vortexjs";
import {OnInit} from "@angular/core";
import {DeviceStatusService} from "@peek/peek_core_device"

@Component({
    selector: "peek-main-app",
    templateUrl: "app.component.web.html",
    styleUrls: ["app.component.web.scss"],
    moduleId: module.id
})
export class AppComponent implements OnInit {

    fullScreen = false;

    constructor(private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                private deviceStatusService:DeviceStatusService) {

    }

    ngOnInit() {
    }

    setBalloonFullScreen(enabled: boolean): void {
        this.fullScreen = enabled;
    }

    showLoading(): boolean {
        return this.deviceStatusService.isLoading;
    }

}

