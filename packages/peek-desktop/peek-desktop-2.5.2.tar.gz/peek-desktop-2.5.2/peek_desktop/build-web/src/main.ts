import {platformBrowserDynamic} from "@angular/platform-browser-dynamic";

import {enableProdMode} from "@angular/core";
import {environment} from "./environments/environment";

import {VortexService} from "@synerty/vortexjs";
const protocol = location.protocol.toLowerCase() == 'https:' ? 'wss' : 'ws';
VortexService.setVortexUrl(`${protocol}://${location.hostname}:${location.port}/vortexws`);
VortexService.setVortexClientName("peek-desktop");

if (environment.production) {
    enableProdMode();
}

import {AppWebModule} from "./app.web.module";
platformBrowserDynamic().bootstrapModule(AppWebModule);

