<script setup lang="ts">
import type { SelectItem } from '@/types/select-item'
import { computed, ref } from 'vue'
import { onClickOutside } from '@vueuse/core'

const props = defineProps<{
    items: SelectItem[]
    selectedItemName: string | null
    placeholder?: string
}>()

const emit = defineEmits<{
    (event: 'update:selectedItemName', newName: string): void
}>()

const listOpened = ref(false)

const selectedItem = computed(() => {
    return props.items.find(item => item.name === props.selectedItemName)
})
function chooseItem(name: string) {
    emit('update:selectedItemName', name)
    listOpened.value = false
}

const selectContainer = ref<HTMLDivElement>()
onClickOutside(selectContainer, () => {
    listOpened.value = false
})
</script>

<template>
    <div class="relative" ref="selectContainer">
        <Transition name="slide-down">
            <ul class="select-list" v-show="listOpened">
                <li v-for="item in items" :key="item.name" class="mb-3 last:mb-0">
                    <button
                        class="text-white"
                        @click="chooseItem(item.name)"
                    >
                        {{ item.label }}
                    </button>
                </li>
            </ul>
        </Transition>

        <button
            class="bg-white border border-neutral-300 rounded-lg px-6 py-3.5
                transition-colors hover:border-neutral-400
                flex items-center gap-x-3.5 outline-neutral-600 min-w-60"
            @click="listOpened = !listOpened"
        >
            <svg
                :class="{
                    'transition-transform duration-300': true,
                    'rotate-180': listOpened
                }"
                width="11"
                height="9"
                viewBox="0 0 11 9" fill="none" xmlns="http://www.w3.org/2000/svg"
            >
                <path d="M1 3L5.5 7L10 3" stroke="#7C7C7C" stroke-width="2" stroke-linecap="round"/>
            </svg>

            <span v-if="selectedItem" class="text-base text-neutral-800">
                {{ selectedItem.label }}
            </span>
            <span v-else class="text-neutral-500">
                {{ placeholder }}
            </span>
        </button>
    </div>
</template>

<style scoped>
.select-list {
    @apply transition-all duration-200 absolute left-0 bg-black/50 w-full p-4 rounded-lg max-h-52
        overflow-y-auto;
    top: calc(100% + 5px);
}

.select-list::-webkit-scrollbar {
    width: 17px;
}

.select-list::-webkit-scrollbar-track {
    background-color: transparent;
}

.select-list::-webkit-scrollbar-thumb {
    background-color: #FFFFFF32;
    border: 5px solid transparent;
    background-clip: padding-box;
    border-radius: 100px;
}
.select-list::-webkit-scrollbar-thumb:hover {
    background-color: #FFFFFF50;
}

.slide-down-enter-from,
.slide-down-leave-to {
    @apply opacity-0 scale-90;
    top: calc(100% - 10px);
}
</style>
