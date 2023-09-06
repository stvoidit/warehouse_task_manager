<template>
    <el-row v-if="store.isAuth">
        <el-col
            :span="24"
            :style="{marginBottom: '2em'}">
            <el-table
                v-loading="store.loading"
                :data="store.tasks_progress"
                :border="true"
                width="100%"
                :flexible="true"
                table-layout="auto">
                <el-table-column
                    v-for="col in columns_tasks_progress"
                    :key="col.prop"
                    :prop="col.prop"
                    :label="col.label"
                    :formatter="col.formatter" />
                <el-table-column label="Остаток">
                    <template #default="{ row }:{ row:frontend.ITaskL }">
                        {{ typeof row.weight === 'number' ? calculationRemainder(row.weight, row.weight_fact) : '-' }}
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
        <el-col :span="24">
            <el-table
                v-loading="store.loading"
                :data="computedDataTasks"
                :border="true"
                :flexible="true"
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
                    <template #default="{ row }:{ row:frontend.ITaskL }">
                        {{ typeof row.weight === 'number' ? calculationRemainder(row.weight, row.weight_fact) : '-' }}
                    </template>
                </el-table-column>
            </el-table>
        </el-col>
    </el-row>
</template>
<script setup lang="ts">
import { onMounted, computed } from "vue";
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
onMounted(async () => {
    store.fetchTasksList(props.stockID);
});

const computedDataTasks = computed(() => {
    const copyArr = [...store.tasks];
    const categoriesCount = new Map<string, number>();
    copyArr.forEach(t => {
        if (categoriesCount.has(t.category)) {
            categoriesCount.set(t.category, (categoriesCount.get(t.category)??0)+1);
        } else {
            categoriesCount.set(t.category, 1);
        }
    });
    return copyArr.map(t => {
        if (categoriesCount.get(t.category) ?? 0 > 1) {
            if (t.weight === 0) {
                t.weight = "-";
            }
        }
        return t;
    });
});

/** Обработчик нажатия на строку таблицы - переход в задачу */
const handleRowClick = (row: frontend.ITaskL) => {
    const qs = (new URLSearchParams({
        tareType: row.tare_type,
        categoryTask: row.category
    })).toString();
    router.push(`/stock/${props.stockID}/task/${row.doc_id}/material/${row.material_id}?${qs}`);
};

function calculationRemainder(weight: number, weight_fact: number) {
    let result = weight - weight_fact;
    if (result < 0) result = 0;
    return result.toLocaleString();
}

/** Список столбцов таблицы */
const dateFormatter = (row: any, col: any, cellValue: string) => dayjs(cellValue, "YYYY-MM-DD").format("DD.MM.YYYY");
const numberFormatter = (row: any, col: any, cellValue: number) => cellValue.toLocaleString();
const columns = [
    {
        prop: "material",
        label: "Материал"
        // width: 200
    },
    {
        prop: "category",
        label: "Категория"
        // width: 100
    },
    {
        prop: "planned_date",
        label: "План. Дата",
        // width: 100,
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
        prop: "weight",
        label: "Задание",
        formatter: numberFormatter
        // width: 100
    },
    {
        prop: "weight_fact",
        label: "Выполнено",
        formatter: numberFormatter
        // width: 100
    }
];
const columns_tasks_progress = [
    {
        prop: "category",
        label: "Категория"
    },
    {
        prop: "material",
        label: "Материал"
    },
    {
        prop: "planned_date",
        label: "План. Дата",
        formatter: dateFormatter
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
        prop: "weight",
        label: "Задание",
        formatter: numberFormatter
    },
    {
        prop: "weight_fact",
        label: "Выполнено",
        formatter: numberFormatter
    }
];
</script>
