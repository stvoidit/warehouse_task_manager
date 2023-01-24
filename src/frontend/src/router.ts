import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";

import LoginPage from "@/Pages/LoginPage.vue";
import TaskPage from "@/Pages/TaskPage.vue";
import TasksListPage from "@/Pages/TasksListPage.vue";
import { useApplicationStore } from "@/store";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "TasksListPage",
        component: TasksListPage
    },
    {
        path: "/login",
        name: "LoginPage",
        component: LoginPage
    },
    {
        path: "/task/:taskID",
        name: "TaskPage",
        component: TaskPage,
        props: route => ({ taskID: (typeof route.params.taskID === "string") ? parseInt(route.params.taskID) : null })
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
// router.isReady().then(async () => {
//     const { registerSW } = await import("virtual:pwa-register");
//     registerSW({ immediate: true });
// });

export default router;
