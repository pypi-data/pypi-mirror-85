import {MainHomeComponent} from "./main-home/main-home.component";
import {UnknownRouteComponent} from "./unknown-route/unknown-route.component";
import {pluginAppRoutes} from "../plugin-app-routes";
import {pluginCfgRoutes} from "../plugin-cfg-routes";

import {DeviceEnrolledGuard} from "@peek/peek_core_device";
import {LoggedInGuard} from "@peek/peek_core_user";

import {MainConfigComponent} from "./main-config/main-config.component";

export const staticRoutes = [
    {
        path: 'peek_core_device',
        loadChildren: "peek_core_device/device.module#DeviceModule"
    },
    {
        path: 'peek_core_user',
        canActivate: [DeviceEnrolledGuard],
        loadChildren: "peek_core_user/plugin-user.module#PluginUserModule"
    },
    // All routes require the device to be enrolled
    {
        path: '',
        canActivate: [DeviceEnrolledGuard, LoggedInGuard],
        children: [
            {
                path: '',
                component: MainHomeComponent
            },
            ...pluginAppRoutes,
            ...pluginCfgRoutes
        ]
    },
    {
        path: 'config',
        component: MainConfigComponent
    },
    {
        path: "**",
        component: UnknownRouteComponent
    }
];
