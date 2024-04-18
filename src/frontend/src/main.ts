import "dayjs/locale/ru";

import { Guide, MessageBox, Tickets, User } from "@element-plus/icons-vue";

import App from "./App.vue";
import ElementPlus from "element-plus";
import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";
import ruLang from "element-plus/es/locale/lang/ru";

const icons = [
    User,
    MessageBox,
    Guide,
    Tickets
];
const pinia = createPinia();
const app = createApp(App);
icons.forEach(component => app.component(component.name as any as string, component));
app.use(pinia);
app.use(router);
app.use(ElementPlus, { locale: ruLang });
app.mount("#app");
