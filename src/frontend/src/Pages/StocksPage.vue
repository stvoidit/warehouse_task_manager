<template>
    <el-row
        v-if="store.isAuth"
        justify="center">
        <el-col
            v-loading="store.loading"
            :span="24"
            :sm="10">
            <el-table
                :data="store.stocks"
                :border="true"
                style="width: 100%"
                table-layout="auto"
                @row-click="handleRowClick">
                <el-table-column
                    v-for="col in columns"
                    :key="col.prop"
                    :prop="col.prop"
                    :label="col.label" />
            </el-table>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import useApplicationStore from "@/store";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useApplicationStore();
/** Получение данных от API со списком складов */
onMounted(async () => {
    await store.fetchStocks();
    if (store.stocks.length === 1) handleRowClick(store.stocks[0]);
});
/** Обработчик нажатия строки таблицы - переход на список заданий на складе */
const handleRowClick = (row: frontend.IStock) => router.push(`/stock/${row.id}`);
/** Список столбцов для таблицы */
const columns = [
    {
        label: "Название",
        prop: "name"
    },
    {
        label: "Кол-во задач",
        prop: "tasks_count"
    }
];
</script>
