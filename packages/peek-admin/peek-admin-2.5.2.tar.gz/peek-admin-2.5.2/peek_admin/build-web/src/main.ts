import {enableProdMode} from '@angular/core';
import { platformBrowserDynamic } from '@angular/platform-browser-dynamic';

import { AppModule } from './app.module';
import {environment} from './environments/environment';

if (environment.production) {
    enableProdMode();
}

import {VortexService} from "@synerty/vortexjs";
const protocol = location.protocol.toLowerCase() == 'https:' ? 'wss' : 'ws';
VortexService.setVortexUrl(`${protocol}://${location.hostname}:${location.port}/vortexws`);
VortexService.setVortexClientName("peek-admin");

platformBrowserDynamic().bootstrapModule(AppModule);
