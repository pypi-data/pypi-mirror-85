import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { NgModule } from "@angular/core";
import { RouterModule } from "@angular/router";
import { BalloonMsgModule } from "@synerty/peek-plugin-base-js";
import {
    TupleActionPushOfflineSingletonService,
    TupleOfflineStorageNameService,
    TupleStorageFactoryService,
    WebSqlFactoryService,
} from "@synerty/vortexjs";
import {
    TupleStorageFactoryServiceWeb,
    WebSqlBrowserFactoryService,
} from "@synerty/vortexjs";
import { staticRoutes } from "./app/app.routes";
import { peekRootServices } from "./app/app.services";
import { AppComponent } from "./app/app.component";
import { MainHomeComponent } from "./app/main-home/main-home.component";
import { MainConfigComponent } from "./app/main-config/main-config.component";
import { MainTitleComponent } from "./app/main-title/main-title.component";
import { MainFooterComponent } from "./app/main-footer/main-footer.component";
import { UnknownRouteComponent } from "./app/unknown-route/unknown-route.component";
import { pluginRootModules } from "./plugin-root-modules";
import { pluginRootServices } from "./plugin-root-services";
import { PluginRootComponent } from "./app/plugin-root.component";
import { en_US, NgZorroAntdModule, NZ_I18N } from "ng-zorro-antd";
import { HttpClientModule } from "@angular/common/http";
import {
    en_US as mobile_en_US,
    LOCAL_PROVIDER_TOKEN,
    NgZorroAntdMobileModule,
} from "ng-zorro-antd-mobile";
import { SearchModule } from "peek_core_search/search.module";
import { registerLocaleData } from "@angular/common";
import en from "@angular/common/locales/en";
import { FormsModule } from "@angular/forms";
import { NzIconModule } from "ng-zorro-antd/icon";

registerLocaleData(en);

export function tupleOfflineStorageNameServiceFactory() {
    return new TupleOfflineStorageNameService("peek_client");
}

@NgModule({
    declarations: [
        AppComponent,
        MainTitleComponent,
        MainFooterComponent,
        MainHomeComponent,
        MainConfigComponent,
        UnknownRouteComponent,
        PluginRootComponent,
    ],
    bootstrap: [AppComponent],
    imports: [
        RouterModule.forRoot(staticRoutes),
        FormsModule,
        NzIconModule,
        BrowserModule,
        BrowserAnimationsModule,
        BalloonMsgModule,
        ...pluginRootModules,
        NgZorroAntdModule,
        NgZorroAntdMobileModule,
        SearchModule,
        HttpClientModule,
    ],
    providers: [
        { provide: NZ_I18N, useValue: en_US },
        { provide: LOCAL_PROVIDER_TOKEN, useValue: mobile_en_US },
        ...peekRootServices,
        {
            provide: WebSqlFactoryService,
            useClass: WebSqlBrowserFactoryService,
        },
        {
            provide: TupleStorageFactoryService,
            useClass: TupleStorageFactoryServiceWeb,
        },
        TupleActionPushOfflineSingletonService,
        ...pluginRootServices,
    ],
})
export class AppWebModule {}
