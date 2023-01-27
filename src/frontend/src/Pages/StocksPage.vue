<template>
    <!-- <pre>{{ store.stocks }}</pre> -->
    <el-row
        v-if="store.isAuth"
        justify="center">
        <el-col
            v-loading="store.loading"
            :span="24"
            :sm="10">
            <el-table
                v-if="store.isAuth"
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

<script lang="ts">
import { defineComponent, onMounted } from "vue";
import { useApplicationStore } from "@/store";
import { useRouter } from "vue-router";
export default defineComponent({
    setup() {
        const router = useRouter();
        const store = useApplicationStore();
        /** Получение данных от API со списком складов */
        onMounted(store.fetchStocks);
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
        return {
            store,
            columns,
            handleRowClick
        };
    }
});
</script>
