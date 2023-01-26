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

    const tasks = shallowRef<Array<frontend.ITaskL>>([]);
    const task = ref<frontend.ITaskP|null>(null);

    const doLogin = (payload: frontend.ILoginPayload) => api.doLogin(payload);
    const fetchTasksList = () => api.fetchTasksList().then(body => tasks.value = body);
    const fetchTask = (taskID: number) => api.fetchTask(taskID).then(body => task.value = body);
    const changePassword = (payload: frontend.IChangePassword) => api.changePasswor(payload);

    const logOut = () => {
        api.currentUser = null;
        api.token = "";
        window.localStorage.removeItem("token");
        location.href = "/login";
    };

    return {
        doLogin,
        fetchTasksList,
        fetchTask,
        tasks,
        task,
        isAuth,
        currentUser,
        checkToken,
        changePassword,
        logOut
    };
});
