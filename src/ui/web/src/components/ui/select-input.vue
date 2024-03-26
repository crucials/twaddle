<script setup lang="ts">
import type { SelectItem } from '@/types/select-item'
import { computed, ref } from 'vue'
import { onClickOutside, onKeyStroke } from '@vueuse/core'
import TextInput from '@/components/ui/text-input.vue'

const props = defineProps<{
    items: SelectItem[]
    selectedItemName: string | null
    placeholder?: string
    searchable?: boolean
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

const searchText = ref('')
const filteredItems = computed(() => {
    const processedSearchText = searchText.value.trim().toUpperCase()
    return props.items.filter(item => item.name.toUpperCase().includes(processedSearchText)
        || item.label.toUpperCase().includes(processedSearchText))
})

const selectContainer = ref<HTMLDivElement>()
onClickOutside(selectContainer, () => {
    listOpened.value = false
})

onKeyStroke('Escape', () => {
    listOpened.value = false
})
</script>

<template>
    <div class="relative" ref="selectContainer">
        <button
            class="bg-white border border-neutral-300 rounded-lg px-6 py-3.5
                transition-colors hover:border-neutral-400
                flex items-center gap-x-3.5 outline-neutral-600 min-w-60 z-20"
            @click="listOpened = !listOpened"
            :aria-expanded="listOpened"
            tabindex="0"
            aria-controls="selectItemList"
            aria-haspopup="listbox"
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

        <Transition name="slide-down">
            <div
                v-show="listOpened"
                class="select-list"
            >
                <TextInput
                    v-if="searchable"
                    v-model="searchText"
                    placeholder="search"
                    class="min-w-full w-full mb-4"
                    size="small"
                />
                
                <ul
                    class="w-full"
                    role="listbox"
                    id="selectItemList"
                >
                    <li
                        v-for="item in filteredItems" :key="item.name"
                        class="block mb-3 last:mb-0"
                        role="option"
                    >
                        <button
                            class="text-white px-2 py-1 rounded-lg hover:bg-white/20 focus:bg-white/30 w-full text-start"
                            @click="chooseItem(item.name)"
                        >
                            {{ item.label }}
                        </button>
                    </li>
                </ul>
            </div>
        </Transition>
    </div>
</template>

<style scoped>
.select-list {
    @apply transition-all duration-200 absolute left-0 bg-black/50 w-full p-4 rounded-lg max-h-52
        overflow-y-auto overflow-x-hidden z-10;
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
