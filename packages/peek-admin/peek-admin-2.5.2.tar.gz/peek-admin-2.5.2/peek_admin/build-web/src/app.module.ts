import { BrowserModule } from "@angular/platform-browser"
import { BrowserAnimationsModule } from "@angular/platform-browser/animations"
import { NgModule } from "@angular/core"
import { FormsModule } from "@angular/forms"
import { BalloonMsgService, BalloonMsgModule } from "@synerty/peek-plugin-base-js"
import {
    TupleStorageFactoryService,
    TupleStorageFactoryServiceWeb,
    VortexService,
    VortexStatusService,
    WebSqlBrowserFactoryService,
    WebSqlFactoryService,
} from "@synerty/vortexjs"
import { AppRoutingModule } from "./app/app-routing.module"
import { AppComponent } from "./app/app.component"
import { DashboardModule } from "./app/dashboard/dashboard.module"
import { NavbarModule } from "./app/navbar/navbar.module"
import { PluginRootComponent } from "./app/plugin-root.component"
import { en_US, NZ_I18N } from "ng-zorro-antd"

import { ACE_CONFIG, AceConfigInterface, AceModule } from "ngx-ace-wrapper"
/** config angular i18n **/
import { registerLocaleData } from "@angular/common"
import en from "@angular/common/locales/en"
import { NzIconModule } from "ng-zorro-antd/icon"
import { HttpClientModule } from "@angular/common/http"

const DEFAULT_ACE_CONFIG: AceConfigInterface = {}

registerLocaleData(en)

@NgModule({
    declarations: [AppComponent, PluginRootComponent],
    imports: [
        AceModule,
        BrowserModule,
        BrowserAnimationsModule,
        FormsModule,
        NzIconModule,
        HttpClientModule,
        AppRoutingModule,
        BalloonMsgModule,
        DashboardModule,
        NavbarModule,
    ],
    providers: [
        {provide: NZ_I18N, useValue: en_US},
        {
            provide: ACE_CONFIG,
            useValue: DEFAULT_ACE_CONFIG,
        },
        {
            provide: WebSqlFactoryService,
            useClass: WebSqlBrowserFactoryService,
        },
        {
            provide: TupleStorageFactoryService,
            useClass: TupleStorageFactoryServiceWeb,
        },
        VortexService,
        VortexStatusService,
        BalloonMsgService,
    ],
    bootstrap: [AppComponent],
})
export class AppModule {
}
