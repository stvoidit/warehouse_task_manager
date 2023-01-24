import { RouteRecordRaw, createRouter, createWebHistory } from "vue-router";

import TaskPage from "@/Pages/TaskPage.vue";
import TasksListPage from "@/Pages/TasksListPage.vue";

const routes: Array<RouteRecordRaw> = [
    {
        path: "/",
        name: "TasksListPage",
        component: TasksListPage
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
// router.isReady().then(async () => {
//     const { registerSW } = await import("virtual:pwa-register");
//     registerSW({ immediate: true });
// });

export default router;
