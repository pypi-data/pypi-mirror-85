import {Component, OnInit} from "@angular/core";
import {ActivatedRoute} from "@angular/router";
import {ITitleBarLink, TitleService} from "@synerty/peek-plugin-base-js";
import {ComponentLifecycleEventEmitter, VortexStatusService} from "@synerty/vortexjs";
import {LoggedInGuard} from "@peek/peek_core_user";

@Component({
    selector: "peek-main-title",
    templateUrl: "main-title.component.web.html",
    styleUrls: ["main-title.component.web.scss"],
    moduleId: module.id
})
export class MainTitleComponent extends ComponentLifecycleEventEmitter implements OnInit {

    private leftLinks = [];
    private rightLinks = [];

    title: string = "Peek";
    isEnabled: boolean = true;
    vortexIsOnline: boolean = false;

    showSearch = false;

    constructor(vortexStatusService: VortexStatusService, titleService: TitleService,
                private loggedInGuard: LoggedInGuard) {
        super();
        this.leftLinks = titleService.leftLinksSnapshot;
        this.rightLinks = titleService.rightLinksSnapshot;

        titleService.title.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.title = v);

        titleService.isEnabled.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.isEnabled = v);

        titleService.leftLinks.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.leftLinks = v);

        titleService.rightLinks.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.rightLinks = v);

        vortexStatusService.isOnline.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.vortexIsOnline = v);

    }

    ngOnInit() {
    }

    // ------------------------------
    // Display methods

    linkTitle(title: ITitleBarLink) {
        if (title.badgeCount == null) {
            return title.text;
        }

        if (title.left) {
            return `${title.text} (${title.badgeCount})`;
        }

        return `(${title.badgeCount}) ${title.text}`;

    }

    showSearchClicked(): void {
        if (this.showSearch == true) {
            this.showSearch = false;
            return;
        }

        const canActivate: any = this.loggedInGuard.canActivate();
        if (canActivate === true)
            this.showSearch = true;
        else if (canActivate.then != null)
            canActivate.then((val: boolean) => this.showSearch = val);
    }
}

