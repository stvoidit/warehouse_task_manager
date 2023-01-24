import "dayjs/locale/ru";
import "element-plus/dist/index.css";

import App from "./App.vue";
import { Download } from "@element-plus/icons-vue";
import ElementPlus from "element-plus";
import { createApp } from "vue";
import { createPinia } from "pinia";
import router from "./router";
import ruLang from "element-plus/es/locale/lang/ru";

const pinia = createPinia();
const app = createApp(App);
app.component(Download.name, Download);
app.use(pinia);
app.use(router);
app.use(ElementPlus, { locale: ruLang });
app.mount("#app");
