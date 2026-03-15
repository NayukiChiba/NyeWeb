<template>
  <el-dialog
    :model-value="modelValue"
    :title="isEdit ? '编辑工具' : '新建工具'"
    width="560px"
    destroy-on-close
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="名称" prop="name">
        <el-input v-model="form.name" clearable placeholder="工具名称"/>
      </el-form-item>
      <el-form-item label="链接" prop="url">
        <el-input v-model="form.url" clearable placeholder="https://example.com"/>
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="form.description" type="textarea" :rows="3" maxlength="500" show-word-limit placeholder="工具描述（可选）"/>
      </el-form-item>
      <el-form-item label="标签">
        <el-select
          v-model="form.tags"
          :reserve-keyword="false"
          allow-create filterable multiple
          placeholder="选择或创建标签"
          style="width: 100%"
        >
          <el-option v-for="tag in allTags" :key="tag" :label="tag" :value="tag"/>
        </el-select>
      </el-form-item>
      <el-form-item v-if="isEdit" label="状态">
        <el-radio-group v-model="form.status">
          <el-radio value="draft">草稿</el-radio>
          <el-radio value="published">已发布</el-radio>
          <el-radio value="recycled">已回收</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">
        {{ isEdit ? '保存修改' : '创建工具' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  modelValue: Boolean,
  tool: { type: Object, default: null },
  allTags: { type: Array, default: () => [] },
  isEdit: Boolean
})

const emit = defineEmits(['update:modelValue', 'success'])

const formRef = ref(null)
const submitting = ref(false)
const form = reactive({
  name: '', url: '', description: '', tags: [], status: 'draft'
})

const rules = {
  name: [{ required: true, message: '请输入工具名称', trigger: 'blur' }],
  url: [
    { required: true, message: '请输入工具链接', trigger: 'blur' },
    { pattern: /^https?:\/\/.+/, message: '请输入有效的URL', trigger: 'blur' }
  ]
}

watch(() => props.modelValue, (val) => {
  if (val && props.isEdit && props.tool) {
    Object.assign(form, {
      name: props.tool.name || '',
      url: props.tool.url || '',
      description: props.tool.description || '',
      tags: Array.isArray(props.tool.tags) ? [...props.tool.tags] : [],
      status: props.tool.status || 'draft'
    })
  } else if (val && !props.isEdit) {
    Object.assign(form, { name: '', url: '', description: '', tags: [], status: 'draft' })
  }
})

const handleSubmit = async () => {
  if (!formRef.value) return
  try {
    await formRef.value.validate()
  } catch { return }

  submitting.value = true
  try {
    if (props.isEdit && props.tool) {
      await axios.put(`/api/tools/${props.tool.id}`, form)
      ElMessage.success('工具更新成功')
    } else {
      await axios.post('/api/tools', form)
      ElMessage.success('工具创建成功')
    }
    emit('update:modelValue', false)
    emit('success')
  } catch (error) {
    ElMessage.error(props.isEdit ? '更新失败' : '创建失败')
  } finally {
    submitting.value = false
  }
}
</script>
