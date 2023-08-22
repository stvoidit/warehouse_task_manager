declare namespace frontend {
    /** Склад */
    export type IStock = {
        id: number
        name: string
        tasks_count: number
    }

    /** Задача для списка */
    export type ITaskL = {
        material: string
        material_id: number
        doc_id: number
        doc_number: string
        planned_date: string
        technical_process: string
        operation: string
        amount: number
        weight: number
        amount_fact: number
        weight_fact: number
        tare_type: string
        category: string
    }

    /** Задание из задачи */
    export type IJob = {
        material_id: string
        material: string
        lab_material_mark: string
        lab_material_group: string
        tare_id: number
        tare_mark: string
        category: string
        tare_type: string
        arrival_tare_amount: number
        arrival_gross_weight: number
        rest_tare_amount: number
        rest_gross_weight: number
        task_tare_amount: number
        task_net_weight: number
        net_weight_fact: number
        done: boolean
    }

    /** Ограничение по весу в категории материала */
    export type ITaskWeight = {
        category: string
        task_weight: number
    }

    /** Задача со списком заданий */
    export type ITaskP = {
        id: number
        doc_number: string
        doc_date: string
        planned_date: string
        stock: number
        technical_process: string
        operation: string
        material: string
        task_weights: Array<ITaskWeight>
        jobs: Array<IJob>
    }

    export type ILoginPayload = {
        login: string;
        password: string;
    }

    export type IChangePassword = {
        newPassword: string;
        repetitionPassword: string;
    }
}
