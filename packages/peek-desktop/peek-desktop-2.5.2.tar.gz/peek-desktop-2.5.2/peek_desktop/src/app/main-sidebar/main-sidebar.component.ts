import { Component } from "@angular/core"
import { homeLinks } from "../../plugin-home-links"
import { IConfigLink, FooterService, NavBackService, ITitleBarLink, TitleService } from "@synerty/peek-plugin-base-js"
import { ComponentLifecycleEventEmitter, VortexStatusService } from "@synerty/vortexjs"
import { LoggedInGuard } from "@peek/peek_core_user"

@Component({
    selector: "peek-main-sidebar",
    templateUrl: "main-sidebar.component.dweb.html",
    styleUrls: ["main-sidebar.component.dweb.scss"],
    moduleId: module.id
})
export class MainSidebarComponent extends ComponentLifecycleEventEmitter {
    
    appDetails = homeLinks
    title: string = "Peek"
    isEnabled: boolean = true
    vortexIsOnline: boolean = false
    configLinks: IConfigLink[] = []
    statusText: string = ""
    showSearch = false
    private leftLinks = []
    private rightLinks = []
    
    constructor(
        vortexStatusService: VortexStatusService,
        footerService: FooterService,
        titleService: TitleService,
        private navBackService: NavBackService,
        private loggedInGuard: LoggedInGuard
    ) {
        super()
        this.leftLinks = titleService.leftLinksSnapshot
        this.rightLinks = titleService.rightLinksSnapshot
        
        titleService.title.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.title = v)
        
        titleService.isEnabled.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.isEnabled = v)
        
        titleService.leftLinks.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.leftLinks = v)
        
        titleService.rightLinks.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.rightLinks = v)
        
        vortexStatusService.isOnline.takeUntil(this.onDestroyEvent)
            .subscribe(v => this.vortexIsOnline = v)
        
        footerService.statusText
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.statusText = v)
        
        this.configLinks = footerService.configLinksSnapshot
        footerService.configLinks
            .takeUntil(this.onDestroyEvent)
            .subscribe(v => this.configLinks = v)
        
    }
    
    ngOnInit() {
    }
    
    // ------------------------------
    // Display methods
    
    isBackButtonEnabled(): boolean {
        return this.navBackService.navBackLen() != 0
    }
    
    linkTitle(title: ITitleBarLink) {
        if (title.badgeCount == null) {
            return title.text
        }
        
        if (title.left) {
            return `${title.text} (${title.badgeCount})`
        }
        
        return `(${title.badgeCount}) ${title.text}`
        
    }
    
    showSearchClicked(): void {
        if (this.showSearch == true) {
            this.showSearch = false
            return
        }
        
        const canActivate: any = this.loggedInGuard.canActivate()
        if (canActivate === true)
            this.showSearch = true
        else if (canActivate.then != null)
            canActivate.then((val: boolean) => this.showSearch = val)
    }
    
    hasConfigLinks(): boolean {
        return this.configLinks != null && this.configLinks.length != 0
    }
    
}

