import { computed, reactive, ref, shallowRef } from "vue";

import ClientAPI from "@/api";
import { defineStore } from "pinia";

// import qs from "qs";

// interface optionsParam {
//     from: string|null;
//     to: string|null;
//     unique?: number;
//     owc?: number
// }
// const qsStringifyOptions: qs.IStringifyOptions = { addQueryPrefix: true, skipNulls: true, arrayFormat: "repeat" };
// const stringifyParams = ({ from, to, ...other }: optionsParam) => qs.stringify({ from, to, ...other }, qsStringifyOptions);

export const useApplicationStore = defineStore("app_store", () => {
    /** http клиент */
    const api = reactive(new ClientAPI());
    const currentUser = computed(() => api.currentUser);
    const isAuth = computed(() => currentUser.value?.can_login === 1);
    const checkToken = () => api.checkToken();

    const stocks = shallowRef<Array<frontend.IStock>>([]);
    const tasks = shallowRef<Array<frontend.ITaskL>>([]);
    const task = ref<frontend.ITaskP | null>(null);
    const loading = ref(false);

    const doLogin = (payload: frontend.ILoginPayload) => api.doLogin(payload);
    const fetchStocks = () => {
        return api.fetchStocks().then(body => stocks.value = body).finally(() => loading.value = false);
    };
    const fetchTasksList = (stockID: number) => {
        loading.value = true;
        return api.fetchTasksList(stockID).then(body => tasks.value = body).finally(() => loading.value = false);
    };
    const fetchTask = (stockID: number, taskID: number, materialID: number) => {
        loading.value = true;
        return api.fetchTask(stockID, taskID, materialID).then(body => task.value = body).finally(() => loading.value = false);
    };
    const changePassword = (payload: frontend.IChangePassword) => {
        loading.value = true;
        return api.changePasswor(payload).finally(() => loading.value = false);
    };
    const updateJobStatus = (taskID: number, materialID: number, taraID: number, done: boolean) => {
        return api.updateJobStatus(taskID, materialID, taraID, done);
    };
    const logOut = () => {
        api.currentUser = null;
        api.token = "";
        window.localStorage.removeItem("token");
        location.href = "/login";
    };

    return {
        doLogin,
        fetchStocks,
        fetchTasksList,
        fetchTask,
        updateJobStatus,
        stocks,
        tasks,
        task,
        isAuth,
        currentUser,
        checkToken,
        changePassword,
        logOut,
        loading
    };
});
