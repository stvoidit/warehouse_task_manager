<template>
    <!-- <pre>{{ store.tasks }}</pre> -->
    <el-table
        v-if="store.isAuth"
        :data="store.tasks"
        :border="true"
        size="small"
        style="width: 100%"
        @row-click="handleRowClick">
        <el-table-column
            v-for="col in columns"
            :key="col.prop"
            :prop="col.prop"
            :label="col.label" />
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
import { onMounted} from "vue";
import { useApplicationStore } from "@/store";
export default {
    setup() {
        const store = useApplicationStore();
        onMounted(store.fetchTasksList);
        const handleRowClick = (row: frontend.ITaskL) => {
            location.href = `/task/${row.doc_id}`;
        };
        const columns = [
            {
                prop: "material",
                label: "material"
            },
            {
                prop: "doc_number",
                label: "doc_number"
            },
            {
                prop: "planned_date",
                label: "planned_date"
            },
            {
                prop: "technical_process",
                label: "technical_process"
            },
            {
                prop: "operation",
                label: "operation"
            },
            {
                prop: "tare_type",
                label: "tare_type"
            },
            {
                prop: "amount",
                label: "amount"
            },
            {
                prop: "weight",
                label: "weight"
            },
            {
                prop: "amount_fact",
                label: "amount_fact"
            },
            {
                prop: "weight_fact",
                label: "weight_fact"
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
