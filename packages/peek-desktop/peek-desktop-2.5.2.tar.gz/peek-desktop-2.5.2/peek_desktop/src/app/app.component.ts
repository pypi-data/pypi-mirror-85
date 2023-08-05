import {Component, OnInit} from "@angular/core";
import {
    ComponentLifecycleEventEmitter,
    VortexService,
    VortexStatusService
} from "@synerty/vortexjs";
import {DeviceStatusService} from "@peek/peek_core_device"
import {UserService} from "@peek/peek_core_user";

@Component({
    selector: "peek-main-app",
    templateUrl: "app.component.dweb.html",
    styleUrls: ["app.component.dweb.scss"],
    moduleId: module.id
})
export class AppComponent extends ComponentLifecycleEventEmitter
    implements OnInit { // Root component

    loggedIn = false;

    constructor(private vortexService: VortexService,
                private vortexStatusService: VortexStatusService,
                private deviceStatusService: DeviceStatusService,
                userService: UserService) {
        super();


        this.loggedIn = userService.loggedIn;
        userService.loggedInStatus
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.loggedIn = v);

    }

    ngOnInit() {
    }

    showLoading(): boolean {
        return this.deviceStatusService.isLoading;
    }

}

