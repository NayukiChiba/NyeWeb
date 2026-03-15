<template>
  <el-dialog :model-value="modelValue" :title="isEdit ? '编辑项目' : '上传项目'" width="560px" destroy-on-close @update:model-value="$emit('update:modelValue', $event)">
    <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item label="名称" prop="name">
        <el-input v-model="form.name" placeholder="项目名称"/>
      </el-form-item>
      <el-form-item label="链接" prop="link">
        <el-input v-model="form.link" placeholder="https://github.com/..."/>
      </el-form-item>
      <el-form-item label="描述">
        <el-input v-model="form.description" type="textarea" :rows="3" placeholder="项目描述"/>
      </el-form-item>
      <el-form-item label="技术栈">
        <el-select v-model="form.tech_stack" :reserve-keyword="false" allow-create filterable multiple placeholder="选择或创建标签" style="width: 100%">
          <el-option v-for="tag in allTags" :key="tag" :label="tag" :value="tag"/>
        </el-select>
      </el-form-item>
      <el-form-item label="状态">
        <el-radio-group v-model="form.status">
          <el-radio value="planning">计划中</el-radio>
          <el-radio value="in-progress">进行中</el-radio>
          <el-radio value="completed">已完成</el-radio>
        </el-radio-group>
      </el-form-item>
      <el-form-item label="可见性">
        <el-switch v-model="form.visibility" :active-value="1" :inactive-value="0" active-text="可见" inactive-text="隐藏"/>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="$emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" :loading="submitting" @click="handleSubmit">{{ isEdit ? '保存' : '创建' }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, watch, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'

const props = defineProps({
  modelValue: Boolean,
  project: { type: Object, default: null },
  allTags: { type: Array, default: () => [] },
  isEdit: Boolean
})
const emit = defineEmits(['update:modelValue', 'success'])
const formRef = ref(null)
const submitting = ref(false)
const form = reactive({ name: '', link: '', description: '', tech_stack: [], status: 'planning', visibility: 1 })

const rules = {
  name: [{ required: true, message: '请输入项目名称', trigger: 'blur' }],
  link: [{ required: true, message: '请输入项目链接', trigger: 'blur' }]
}

watch(() => props.modelValue, (val) => {
  if (val && props.isEdit && props.project) {
    Object.assign(form, {
      name: props.project.name || '',
      link: props.project.link || '',
      description: props.project.description || '',
      tech_stack: Array.isArray(props.project.tech_stack) ? [...props.project.tech_stack] : [],
      status: props.project.status || 'planning',
      visibility: props.project.visibility ?? 1
    })
  } else if (val) {
    Object.assign(form, { name: '', link: '', description: '', tech_stack: [], status: 'planning', visibility: 1 })
  }
})

const handleSubmit = async () => {
  if (!formRef.value) return
  try { await formRef.value.validate() } catch { return }
  submitting.value = true
  try {
    if (props.isEdit && props.project) {
      await axios.put(`/api/projects/${props.project.id}`, form)
      ElMessage.success('项目更新成功')
    } else {
      await axios.post('/api/projects', form)
      ElMessage.success('项目创建成功')
    }
    emit('update:modelValue', false)
    emit('success')
  } catch { ElMessage.error(props.isEdit ? '更新失败' : '创建失败') }
  finally { submitting.value = false }
}
</script>
