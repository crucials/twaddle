<script setup lang="ts">
import SelectInput from '@/components/ui/select-input.vue';
import { useNotificationsStore } from '@/stores/notifications'
import { ref } from 'vue'
import { EelResponse } from '@/types/eel-response'
import { SelectItem } from '@/types/select-item'

interface AudioDevice {
    name: string
    index: number
}

const props = defineProps<{
    modelValue: string | null
}>()
const emit = defineEmits<{
    (event: 'update:modelValue', newValue: string): void
}>()

const { showNotification } = useNotificationsStore()

const items = ref<SelectItem[]>([])
await updateDevices()

async function updateDevices() {
    const devicesResponse: EelResponse<AudioDevice[]> = await eel.getRecordingDevices()()
    
    if(devicesResponse.error || !devicesResponse.data) {
        const errorNotificationText = devicesResponse.error ?
            'failed to load input devices: ' + devicesResponse.error.explanation :
            'failed to load input devices'

        showNotification({
            type: 'error',
            text: errorNotificationText
        })

        return
    }

    items.value = devicesResponse.data.map(device => {
        return { label: device.name, name: `${device.index}` }
    })
}
</script>

<template>
    <label class="flex-grow max-w-64 min-w-52">
        <div class="mb-1">
            recording device
        </div>
        <SelectInput
            placeholder="default"
            :items="items"
            :selected-item-name="modelValue"
            @update:selectedItemName="(newValue: string) => emit('update:modelValue', newValue)"
        />
    </label>
</template>
