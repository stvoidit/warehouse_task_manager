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
    const task = ref<frontend.ITaskP|null>(null);

    const doLogin = (payload: frontend.ILoginPayload) => api.doLogin(payload);
    const fetchStocks = () => api.fetchStocks().then(body => stocks.value = body);
    const fetchTasksList = (stockID: number) => api.fetchTasksList(stockID).then(body => tasks.value = body);
    const fetchTask = (stockID: number, taskID: number, materialID: number) => api.fetchTask(stockID, taskID, materialID).then(body => task.value = body);
    const changePassword = (payload: frontend.IChangePassword) => api.changePasswor(payload);

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
        stocks,
        tasks,
        task,
        isAuth,
        currentUser,
        checkToken,
        changePassword,
        logOut
    };
});
