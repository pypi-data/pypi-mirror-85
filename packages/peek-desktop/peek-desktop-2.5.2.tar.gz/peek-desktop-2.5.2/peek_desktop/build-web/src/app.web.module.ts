import { BrowserModule } from "@angular/platform-browser"
import { BrowserAnimationsModule } from "@angular/platform-browser/animations"
import { NgModule } from "@angular/core"
import { FormsModule } from "@angular/forms"
import { NzIconModule } from "ng-zorro-antd/icon"
import { RouterModule } from "@angular/router"
import { HttpClientModule } from "@angular/common/http"
import { BalloonMsgModule } from "@synerty/peek-plugin-base-js"
import {
    TupleActionPushOfflineSingletonService,
    TupleDataObservableNameService,
    TupleOfflineStorageNameService,
    TupleStorageFactoryService,
    TupleStorageFactoryServiceWeb,
    WebSqlBrowserFactoryService,
    WebSqlFactoryService,
} from "@synerty/vortexjs"
import { staticRoutes } from "./app/app.routes"
import { peekRootServices } from "./app/app.services"
import { AppComponent } from "./app/app.component"
import { MainHomeComponent } from "./app/main-home/main-home.component"
import { MainConfigComponent } from "./app/main-config/main-config.component"
import { MainSidebarComponent } from "./app/main-sidebar/main-sidebar.component"
import { UnknownRouteComponent } from "./app/unknown-route/unknown-route.component"
import { pluginRootModules } from "./plugin-root-modules"
import { pluginRootServices } from "./plugin-root-services"
import { PluginRootComponent } from "./app/plugin-root.component"
import { en_US, NgZorroAntdModule, NZ_I18N } from "ng-zorro-antd"
import { registerLocaleData } from "@angular/common"
import en from "@angular/common/locales/en"
import { SearchModule } from "peek_core_search/search.module"

registerLocaleData(en)

export function tupleDataObservableNameServiceFactory() {
    return new TupleDataObservableNameService("peek_client", {
        plugin: "peek_client",
    })
}

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService("peek_client")
}

@NgModule({
    declarations: [
        AppComponent,
        MainHomeComponent,
        MainConfigComponent,
        MainSidebarComponent,
        UnknownRouteComponent,
        PluginRootComponent,
    ],
    bootstrap: [AppComponent],
    imports: [
        RouterModule.forRoot(staticRoutes),
        BrowserModule,
        BrowserAnimationsModule,
        HttpClientModule,
        FormsModule,
        NzIconModule,
        BalloonMsgModule,
        ...pluginRootModules,
        NgZorroAntdModule,
        SearchModule,
    ],
    providers: [
        {provide: NZ_I18N, useValue: en_US},
        {
            provide: WebSqlFactoryService,
            useClass: WebSqlBrowserFactoryService,
        },
        {
            provide: TupleStorageFactoryService,
            useClass: TupleStorageFactoryServiceWeb,
        },
        TupleActionPushOfflineSingletonService,
        
        ...peekRootServices,
        ...pluginRootServices,
    ],
})
export class AppWebModule {
}
