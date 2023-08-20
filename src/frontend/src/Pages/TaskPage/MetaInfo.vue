<template>
    <el-row
        class="mb sticky-row"
        :gutter="20">
        <el-col :span="24">
            <span style="font-size: 1.4em;"><b>{{ docNumber }} - {{ material }}</b></span>
        </el-col>
        <el-col v-bind="colAttr">
            <el-table
                class="mt"
                :data="metaInfo.data"
                :border="true"
                :fit="false"
                :show-header="true"
                table-layout="fixed">
                <el-table-column
                    v-for="field in metaInfo.fields"
                    :key="field.prop"
                    :prop="field.prop"
                    :label="field.label"
                    :width="150" />
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
