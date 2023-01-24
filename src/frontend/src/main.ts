import "dayjs/locale/ru";
import "element-plus/dist/index.css";

import { MessageBox, User } from "@element-plus/icons-vue";

import App from "./App.vue";
import ElementPlus from "element-plus";
import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";
import ruLang from "element-plus/es/locale/lang/ru";

const pinia = createPinia();
const app = createApp(App);
[
    User,
    MessageBox
].forEach(component => app.component(component.name, component));
app.use(pinia);
app.use(router);
app.use(ElementPlus, { locale: ruLang });
app.mount("#app");
