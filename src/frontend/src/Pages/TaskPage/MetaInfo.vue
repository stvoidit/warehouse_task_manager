<template>
    <el-row
        class="mb sticky-row"
        :gutter="10">
        <el-col v-bind="colAttr">
            <el-table
                class="mt"
                :style="{fontSize: '16px'}"
                :data="metaInfo.data"
                :border="true"
                :fit="true"
                :show-header="true"
                table-layout="auto">
                <el-table-column
                    v-for="field in metaInfo.fields"
                    :key="field.prop"
                    :prop="field.prop"
                    :label="field.label" />
            </el-table>
        </el-col>
        <el-col v-bind="colAttr">
            <slot />
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { PropType } from "vue";
interface IMetaInfo {
    fields: {
        label: string;
        prop: string;
        width: number;
    }[];
    data: {
        material?: string;
        technical_process?: string;
        operation?: string;
        tareType: string;
        planned_date: string;
    }[];
}
defineProps({
    metaInfo: {
        type: Object as PropType<IMetaInfo>,
        required: true
    },
    docNumber: {
        type: String,
        required: true
    },
    material: {
        type: String,
        required: true
    }
});
const colAttr = {
    xs: 24,
    sm: 24,
    md: 12,
    lg: 12,
    xl: 12
};
</script>
