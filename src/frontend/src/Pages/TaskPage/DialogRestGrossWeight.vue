<template>
    <el-dialog
        v-model="visible"
        destroy-on-close
        :show-close="false"
        title="Введите остаток веса брутто и/или укажите дополнительный вид обработки материала"
        :align-center="true"
        :width="isLandscape ? '33%': '100%'">
        <el-form
            v-if="job"
            label-position="top">
            <el-form-item label="Остаток (брутто)">
                <el-input-number
                    v-model="rest_gross_weight"
                    size="large"
                    :precision="2"
                    :min="0" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="visible = false">
                    Закрыть
                </el-button>
                <el-button
                    type="success"
                    @click="onConfirm">
                    Подтвердить
                </el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup lang="ts">
import { computed, PropType } from "vue";
const props = defineProps({
    dialogVisible: {
        type: Boolean,
        required: true
    },
    job: {
        type: Object as PropType<frontend.IJob|null>,
        required: true
    },
    isLandscape: {
        type: Boolean,
        default: true
    }
});
const emit = defineEmits<{
    "update:dialogVisible": [value: boolean],
    "changeRGW": [value: frontend.IJob],
    "update:job": [value: frontend.IJob],
}>();

const visible = computed({
    get: () => props.dialogVisible,
    set: (value: boolean) => {
        emit("update:dialogVisible", value);
    }
});

const rest_gross_weight = computed({
    get: () => props.job?.rest_gross_weight,
    set: (value: number) => {
        const jobCopy = { ...props.job };
        jobCopy.rest_gross_weight = value;
        emit("update:job", jobCopy);
    }
});

const onConfirm = () => {
    if (props.job !== null) {
        emit("changeRGW", props.job);
    }
    visible.value = false;
};
</script>
