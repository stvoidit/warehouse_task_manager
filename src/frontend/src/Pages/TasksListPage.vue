<template>
    <!-- <pre>{{ store.tasks }}</pre> -->
    <el-table
        v-if="store.isAuth"
        v-loading="store.loading"
        :data="store.tasks"
        :border="true"
        table-layout="auto"
        @row-click="handleRowClick">
        <el-table-column
            v-for="col in columns"
            :key="col.prop"
            :prop="col.prop"
            :label="col.label"
            :min-width="col.width"
            :formatter="col.formatter" />
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
import dayjs from "dayjs";
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
        const dateDormatter = (row, column, cellValue: string) => dayjs(cellValue, "YYYY-MM-DD").format("DD.MM.YYYY");
        const columns = [
            {
                prop: "material",
                label: "Материал",
                width: 200
            },
            {
                prop: "doc_number",
                label: "Задание",
                width: 100
            },
            {
                prop: "planned_date",
                label: "План. Дата",
                width: 100,
                formatter: dateDormatter
            },
            {
                prop: "technical_process",
                label: "Техпроцесс",
                width: 100
            },
            {
                prop: "operation",
                label: "Операция",
                width: 200
            },
            {
                prop: "tare_type",
                label: "Тара",
                width: 100
            },
            {
                prop: "amount",
                label: "Кол-во",
                width: 100
            },
            {
                prop: "weight",
                label: "Вес",
                width: 100
            },
            {
                prop: "amount_fact",
                label: "Факт кол-во",
                width: 120
            },
            {
                prop: "weight_fact",
                label: "Факт вес",
                width: 100
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
