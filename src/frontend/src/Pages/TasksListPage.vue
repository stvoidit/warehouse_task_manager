<template>
    <el-container>
        <el-main>
            <!-- <pre>{{ store.tasks }}</pre> -->
            <el-table
                :data="store.tasks"
                :border="true"
                style="width: 100%"
                @row-click="handleRowClick">
                <el-table-column
                    v-for="col in columns"
                    :key="col.prop"
                    :prop="col.prop"
                    :label="col.label" />
            </el-table>
        </el-main>
    </el-container>
</template>
<script lang="ts">
import { onMounted} from "vue";
import { useApplicationStore } from "@/store";

export default {
    components: {

    },
    setup() {
        const store = useApplicationStore();
        onMounted(store.fetchTasksList);
        const handleRowClick = (row: frontend.ITaskL) => {
            location.href = `/task/${row.doc_id}`;
        };
        const columns = [
            {
                prop: "planned_date",
                label: "Запланированная дата"
            },
            {
                prop: "material",
                label: "Материал"
            },
            {
                prop: "place?",
                label: "Место хранения/Участок (?)"
            },
            {
                prop: "operation",
                label: "Операция"
            },
            {
                prop: "doc_number",
                label: "Задание"
            },
            {
                prop: "amount_fact",
                label: "Выполнено"
            },
            {
                prop: "amount",
                label: "Всего заданий (?)"
            },
            {
                prop: "weight",
                label: "Вес всего"
            },
            {
                prop: "weight_fact",
                label: "Вес выполнено (?)"
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
