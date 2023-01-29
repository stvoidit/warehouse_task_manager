<template>
    <!-- <pre>{{ store.tasks }}</pre> -->
    <el-table
        v-if="store.isAuth"
        v-loading="store.loading"
        :data="store.tasks"
        :border="true"
        table-layout="auto"
        size="small"
        @row-click="handleRowClick">
        <el-table-column
            v-for="col in columns"
            :key="col.prop"
            :prop="col.prop"
            :label="col.label"
            :width="col.width" />
        <el-table-column label="Остаток кол-во">
            <template #default="scope">
                {{ scope.row.amount - scope.row.amount_fact }}
            </template>
        </el-table-column>
        <el-table-column label="Остаток вес">
            <template #default="scope">
                {{ scope.row.weight - scope.row.weight_fact }}
            </template>
        </el-table-column>
    </el-table>
</template>
<script lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useApplicationStore } from "@/store";
export default {
    props: {
        /** ID склада */
        stockID: { type: Number, required: true }
    },
    setup(props) {
        const router = useRouter();
        const store = useApplicationStore();
        /** Получени от API списка задач на складе */
        onMounted(() => store.fetchTasksList(props.stockID));
        /** Обработчик нажатия на строку таблицы - переход в задачу */
        const handleRowClick = (row: frontend.ITaskL) => router.push(`/stock/${props.stockID}/task/${row.doc_id}/material/${row.material_id}`);
        /** Список столбцов таблицы */
        const columns = [
            {
                prop: "material",
                label: "Материал",
                width: 100
            },
            {
                prop: "doc_number",
                label: "Задание"
            },
            {
                prop: "planned_date",
                label: "План. Дата"
            },
            {
                prop: "technical_process",
                label: "Техпроцесс"
            },
            {
                prop: "operation",
                label: "Операция"
            },
            {
                prop: "tare_type",
                label: "Тара"
            },
            {
                prop: "amount",
                label: "Кол-во"
            },
            {
                prop: "weight",
                label: "Вес"
            },
            {
                prop: "amount_fact",
                label: "Факт кол-во"
            },
            {
                prop: "weight_fact",
                label: "Факт вес"
            }
        ];
        return {
            store,
            columns,
            handleRowClick
        };
    }
};
</script>
<style>

</style>
