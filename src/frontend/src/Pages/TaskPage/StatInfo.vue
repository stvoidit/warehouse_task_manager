<template>
    <el-row :gutter="20">
        <el-col
            v-for="cat in statInfo"
            :key="cat.categoryLabel"
            class="mb"
            v-bind="colAttr">
            <div :style="{minHeight: '1.3rem'}">
                <b>{{ cat.categoryLabel }}</b>
            </div>
            <el-table
                :data="cat.data"
                :border="true"
                :show-header="false"
                table-layout="auto">
                <el-table-column
                    prop="label"
                    :width="150" />
                <el-table-column
                    prop="count" />
                <el-table-column
                    prop="netWeight" />
            </el-table>
        </el-col>
    </el-row>
</template>

<script setup lang="ts">
import { PropType } from "vue";
interface IStatInfo {
    categoryLabel: string;
    data: {
        label: string;
        count: number | undefined;
        netWeight: number | undefined;
    }[];
}[];
defineProps({
    statInfo: {
        type: Array as PropType<IStatInfo[]>,
        required: true
    }
});
const colAttr = {
    xs:24,
    sm:12,
    md:12,
    lg:8,
    xl:6
};
</script>
