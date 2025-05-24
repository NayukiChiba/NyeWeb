<template>
  <el-dialog
      :before-close="handleClose"
      :close-on-click-modal="false"
      :model-value="modelValue"
      title="编辑项目"
      width="700px"
      @update:model-value="$emit('update:modelValue', $event)"
  >
    <el-form ref="formRef" :model="formData" :rules="formRules" label-width="100px">
      <!-- 项目名称 -->
      <el-form-item label="项目名称" prop="name" required>
        <el-input
            v-model="formData.name"
            maxlength="255"
            placeholder="请输入项目名称"
            show-word-limit
        />
      </el-form-item>

      <!-- 项目GitHub链接 -->
      <el-form-item label="GitHub链接" prop="link" required>
        <el-input
            v-model="formData.link"
            placeholder="https://github.com/..."
        />
      </el-form-item>

      <!-- 项目描述 -->
      <el-form-item label="项目描述" prop="description">
        <el-input
            v-model="formData.description"
            :rows="4"
            maxlength="500"
            placeholder="请输入项目描述"
            show-word-limit
            type="textarea"
        />
      </el-form-item>

      <!-- 技术栈 -->
      <el-form-item label="技术栈">
        <el-select
            v-model="formData.techStack"
            :multiple-limit="10"
            allow-create
            filterable
            multiple
            placeholder="选择或输入技术栈"
            style="width: 100%"
        >
          <el-option
              v-for="tag in existingTags"
              :key="tag"
              :label="tag"
              :value="tag"
          />
        </el-select>
      </el-form-item>

      <!-- 项目状态 -->
      <el-form-item label="项目状态" prop="status">
        <el-radio-group v-model="formData.status">
          <el-radio value="planning">计划中</el-radio>
          <el-radio value="in-progress">进行中</el-radio>
          <el-radio value="completed">已完成</el-radio>
        </el-radio-group>
      </el-form-item>

      <!-- 可见性 -->
      <el-form-item label="可见性" prop="visibility">
        <el-radio-group v-model="formData.visibility">
          <el-radio value="draft">草稿</el-radio>
          <el-radio value="published">发布</el-radio>
        </el-radio-group>
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="handleClose">取消</el-button>
        <el-button :loading="updating" type="primary" @click="handleUpdate">
          <el-icon>
            <Check/>
          </el-icon>
          更新项目
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import {onMounted, reactive, ref, watch} from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import {Check, Edit, Upload as UploadIcon} from '@element-plus/icons-vue'
import axios from 'axios'

const props = defineProps({
  modelValue: Boolean,
  project: Object
})

const emit = defineEmits(['update:modelValue', 'update-success'])

const formData = reactive({
  name: '',
  link: '',
  description: '',
  techStack: [],
  status: 'planning',
  visibility: 'draft',
})

const formRules = {
  name: [
    {required: true, message: '请输入项目名称', trigger: 'blur'},
    {min: 1, max: 255, message: '名称长度应在1-255个字符之间', trigger: 'blur'}
  ],
  link: [
    {required: true, message: '请输入GitHub链接', trigger: 'blur'},
    {pattern: /^https?:\/\/.+/, message: '请输入有效的URL', trigger: 'blur'}
  ],
  status: [
    {required: true, message: '请选择项目状态', trigger: 'change'}
  ]
}

const formRef = ref(null)
const existingTags = ref([])
const updating = ref(false)
const hasChanges = ref(false)

// 监听项目数据变化，初始化表单
watch(() => props.project, (newProject) => {
  if (newProject && props.modelValue) {
    initializeForm(newProject)
  }
}, {immediate: true})

const initializeForm = (project) => {
  Object.assign(formData, {
    name: project.name || '',
    link: project.link || '',
    description: project.description || '',
    techStack: Array.isArray(project.techStack) ? [...project.techStack] : [],
    status: project.status || 'planning',
    visibility: project.visibility || 'draft',
  })
  hasChanges.value = false
}

// 监听表单数据变化
watch(() => [formData.name, formData.link, formData.description, formData.techStack, formData.status, formData.visibility], () => {
  hasChanges.value = true
}, {deep: true})

const fetchTags = async () => {
  try {
    const res = await axios.get('/api/project-tags')
    if (res.data?.tags && Array.isArray(res.data.tags)) {
      existingTags.value = res.data.tags
    } else {
      existingTags.value = []
    }
  } catch (error) {
    console.error('获取标签失败:', error)
    existingTags.value = []
  }
}



const handleUpdate = async () => {
  if (!formRef.value) return

  try {
    await formRef.value.validate()

    updating.value = true

    const updateData = {
      name: formData.name,
      link: formData.link,
      description: formData.description,
      tech_stack: formData.techStack,
      status: formData.status,
      visibility: formData.visibility,
    }

    await axios.put(`/api/projects/${props.project.id}`, updateData)

    ElMessage.success('项目更新成功')
    hasChanges.value = false
    emit('update-success')
    emit('update:modelValue', false)
  } catch (error) {
    console.error('更新失败:', error)
    handleUpdateError(error)
  } finally {
    updating.value = false
  }
}

const handleUpdateError = (error) => {
  if (error.response?.status === 409) {
    ElMessage.error('项目标题已存在')
  } else if (error.response?.status === 400) {
    ElMessage.error(error.response.data?.detail || '请求参数错误')
  } else if (error.response?.status === 404) {
    ElMessage.error('项目不存在或已被删除')
  } else if (error.response?.status === 405) {
    ElMessage.error('服务器不支持此操作，请联系管理员')
  } else {
    ElMessage.error('更新失败: ' + (error.response?.data?.detail || error.message))
  }
}

const handleClose = () => {
  if (hasChanges.value) {
    ElMessageBox.confirm(
        '确定要关闭吗？未保存的修改将丢失。',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
    ).then(() => {
      resetForm()
      emit('update:modelValue', false)
    }).catch(() => {
    })
  } else {
    resetForm()
    emit('update:modelValue', false)
  }
}

const resetForm = () => {
  if (uploadRef.value) {
    uploadRef.value.clearFiles()
  }
  if (formRef.value) {
    formRef.value.resetFields()
  }
  hasChanges.value = false
}

onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.upload-section {
  width: 100%;
}

.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}

.dialog-footer {
  text-align: right;
}

.el-button {
  border-radius: 6px;
  font-weight: 500;
}

.el-button--primary {
  background: #409eff;
  border-color: #409eff;
}

:deep(.el-form-item__label) {
  font-weight: 500;
}

:deep(.el-input__inner) {
  border-radius: 6px;
}

:deep(.el-textarea__inner) {
  border-radius: 6px;
}

:deep(.el-select .el-input__inner) {
  border-radius: 6px;
}
</style>
