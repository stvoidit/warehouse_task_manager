import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";

import useApplicationStore from "@/store";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/login",
        component: () => import("@/Pages/LoginPage.vue")
    },
    {
        path: "/",
        component: () => import("@/Pages/StocksPage.vue")
    },
    {
        path: "/stock/:stockID",
        component: () => import("@/Pages/TasksListPage.vue"),
        props: route => ({
            stockID: (typeof route.params.stockID === "string") ? parseInt(route.params.stockID) : null
        })
    },
    {
        path: "/stock/:stockID/task/:taskID/material/:materialID",
        component: () => import("@/Pages/TaskPage/index.vue"),
        props: route => ({
            stockID: (typeof route.params.stockID === "string") ? parseInt(route.params.stockID) : null,
            taskID: (typeof route.params.taskID === "string") ? parseInt(route.params.taskID) : null,
            materialID: (typeof route.params.materialID === "string") ? parseInt(route.params.materialID) : null
        })
    }
];
const router = createRouter({
    history: createWebHistory(),
    routes: routes
});
/** проверка токена перед каждым переходом на страницу */
router.beforeEach(() => useApplicationStore().checkToken());
/** обертка для PWA */
router.isReady().then(async () => {
    const { registerSW } = await import("virtual:pwa-register");
    registerSW({ immediate: true });
});

export default router;
