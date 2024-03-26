<script setup lang="ts">
withDefaults(defineProps<{
    modelValue: string
    size?: 'small' | 'medium'
    icon?: string
}>(), { size: 'medium' })

const emit = defineEmits<{
    (event: 'update:modelValue', newValue: string): void
}>()
</script>

<template>
    <input
        :value="modelValue"
        type="text"
        class="text-input bg-white rounded-lg text-neutral-800 transition-colors
            min-w-60 flex items-center gap-x-3.5 outline-neutral-800 bg-no-repeat"
        :class="{
            'px-4 py-3.5 text-base': size === 'medium',
            'px-2.5 py-1.5 text-base': size === 'small'
        }"
        @input="event => emit('update:modelValue', (event.target as HTMLInputElement).value)"
    />
</template>

<style scoped>
.text-input {
    background-position-x: 16px;
    background-position-y: center;
}
</style>
