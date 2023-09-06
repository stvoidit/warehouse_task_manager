<template>
    <el-row v-if="store.isAuth">
        <el-table
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
            <el-table-column label="Остаток">
                <template #default="scope">
                    {{ scope.row.weight - scope.row.weight_fact }}
                </template>
            </el-table-column>
        </el-table>
    </el-row>
</template>
<script setup lang="ts">
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import useApplicationStore from "@/store";
import dayjs from "dayjs";

const props = defineProps({
    /** ID склада */
    stockID: { type: Number, required: true }
});
const router = useRouter();
const store = useApplicationStore();
/** Получени от API списка задач на складе */
onMounted(() => store.fetchTasksList(props.stockID));
/** Обработчик нажатия на строку таблицы - переход в задачу */
const handleRowClick = (row: frontend.ITaskL) => {
    const qs = (new URLSearchParams({
        tareType: row.tare_type,
        categoryTask: row.category
    })).toString();
    router.push(`/stock/${props.stockID}/task/${row.doc_id}/material/${row.material_id}?${qs}`);
};
/** Список столбцов таблицы */
const dateFormatter = (row: any, col: any, cellValue: string) => dayjs(cellValue, "YYYY-MM-DD").format("DD.MM.YYYY");
const columns = [
    {
        prop: "material",
        label: "Материал",
        width: 200
    },
    {
        prop: "planned_date",
        label: "План. Дата",
        width: 100,
        formatter: dateFormatter
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
        prop: "category",
        label: "Категория",
        width: 100
    },
    {
        prop: "weight",
        label: "Задание",
        width: 100
    },
    {
        prop: "weight_fact",
        label: "Выполнено",
        width: 100
    }
];
</script>
