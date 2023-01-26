import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/Pages/LoginPage.vue";
import StocksPage from "@/Pages/StocksPage.vue";
import TaskPage from "@/Pages/TaskPage.vue";
import TasksListPage from "@/Pages/TasksListPage.vue";
import { useApplicationStore } from "@/store";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/login",
        name: "LoginPage",
        component: LoginPage
    },
    {
        path: "/",
        name: "StocksPage",
        component: StocksPage
    },
    {
        path: "/stock/:stockID",
        name: "TasksListPage",
        component: TasksListPage,
        props: route => ({
            stockID: (typeof route.params.stockID === "string") ? parseInt(route.params.stockID) : null
        })
    },
    {
        path: "/stock/:stockID/task/:taskID/material/:materialID",
        name: "TaskPage",
        component: TaskPage,
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
router.beforeEach(() => {
    const store = useApplicationStore();
    store.checkToken();
});
router.isReady().then(async () => {
    const { registerSW } = await import("virtual:pwa-register");
    registerSW({ immediate: true });
});

export default router;
