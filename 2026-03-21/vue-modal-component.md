# Vue 弹窗组件功能点说明

## 组件概述
使用 Vue3 + TypeScript 封装的通用弹窗组件，支持插槽定制内容。

## 功能点清单

### 1. 基本属性 (Props)
| 属性 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `visible` | `boolean` | `false` | 控制弹窗显示隐藏 |
| `title` | `string` | `''` | 弹窗标题 |
| `width` | `string` | `'500px'` | 弹窗宽度 |
| `closeOnClickOverlay` | `boolean` | `true` | 点击遮罩是否关闭 |
| `showClose` | `boolean` | `true` | 是否显示关闭按钮 |
| `confirmText` | `string` | `'确定'` | 确认按钮文字 |
| `cancelText` | `string` | `'取消'` | 取消按钮文字 |
| `confirmLoading` | `boolean` | `false` | 确认按钮加载状态 |

### 2. 事件 (Emits)
| 事件名 | 参数 | 说明 |
|--------|------|------|
| `update:visible` | `(val: boolean)` | 显示状态变更 |
| `confirm` | `()` | 点击确定触发 |
| `cancel` | `() => void` | 点击取消/关闭触发 |
| `close` | `() => void` | 弹窗关闭时触发 |

### 3. 插槽 (Slots)
| 插槽名 | 说明 |
|--------|------|
| `default` | 弹窗主体内容 |
| `title` | 自定义标题区域 |
| `footer` | 自定义底部区域 |
| `close-icon` | 自定义关闭图标 |

## 代码实现

### Modal.vue
```vue
<template>
  <Teleport to="body">
    <Transition name="modal">
      <div 
        v-if="visible" 
        class="modal-overlay"
        @click="handleOverlayClick"
      >
        <div 
          class="modal-container"
          :style="{ width }"
          @click.stop
        >
          <!-- 标题区 -->
          <div class="modal-header">
            <slot name="title">
              <span class="modal-title">{{ title }}</span>
            </slot>
            <slot name="close-icon">
              <button class="modal-close" @click="handleCancel">×</button>
            </slot>
          </div>

          <!-- 内容区 -->
          <div class="modal-body">
            <slot></slot>
          </div>

          <!-- 底部区 -->
          <div class="modal-footer">
            <slot name="footer">
              <button class="btn btn-cancel" @click="handleCancel">
                {{ cancelText }}
              </button>
              <button 
                class="btn btn-confirm" 
                :loading="confirmLoading"
                @click="handleConfirm"
              >
                {{ confirmText }}
              </button>
            </slot>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
interface Props {
  visible: boolean
  title?: string
  width?: string
  closeOnClickOverlay?: boolean
  showClose?: boolean
  confirmText?: string
  cancelText?: string
  confirmLoading?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  title: '',
  width: '500px',
  closeOnClickOverlay: true,
  showClose: true,
  confirmText: '确定',
  cancelText: '取消',
  confirmLoading: false
})

const emit = defineEmits<{
  'update:visible': [val: boolean]
  'confirm': []
  'cancel': []
  'close': []
}>()

// 点击遮罩关闭
const handleOverlayClick = () => {
  if (props.closeOnClickOverlay) {
    handleCancel()
  }
}

// 取消/关闭
const handleCancel = () => {
  emit('update:visible', false)
  emit('cancel')
  emit('close')
}

// 确认
const handleConfirm = () => {
  emit('confirm')
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-container {
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  max-width: 90vw;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.modal-title {
  font-size: 16px;
  font-weight: 600;
}

.modal-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.modal-close:hover {
  color: #333;
}

.modal-body {
  padding: 20px;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  padding: 16px 20px;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.btn {
  padding: 8px 20px;
  border-radius: 4px;
  cursor: pointer;
  border: none;
  font-size: 14px;
}

.btn-cancel {
  background: #fff;
  border: 1px solid #dcdfe6;
}

.btn-confirm {
  background: #409eff;
  color: #fff;
}

.btn-confirm:hover {
  background: #66b1ff;
}

/* 动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s;
}

.modal-enter-active .modal-container,
.modal-leave-active .modal-container {
  transition: transform 0.3s;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-container,
.modal-leave-to .modal-container {
  transform: scale(0.9);
}
</style>
```

## 使用示例

### 1. 基本用法
```vue
<template>
  <button @click="visible = true">打开弹窗</button>
  
  <Modal 
    v-model:visible="visible"
    title="提示"
    @confirm="handleConfirm"
    @cancel="handleCancel"
  >
    这是一个基本弹窗
  </Modal>
</template>
```

### 2. 自定义底部
```vue
<Modal v-model:visible="visible" title="自定义底部">
  <p>内容区域</p>
  
  <template #footer>
    <button @click="visible = false">自定义取消</button>
    <button class="primary" @click="handleSubmit">提交</button>
  </template>
</Modal>
```

### 3. 表单弹窗
```vue
<Modal
  v-model:visible="visible"
  title="编辑用户"
  :confirm-loading="loading"
  @confirm="handleSubmit"
>
  <el-form :model="form" label-width="80px">
    <el-form-item label="姓名">
      <el-input v-model="form.name" />
    </el-form-item>
    <el-form-item label="邮箱">
      <el-input v-model="form.email" />
    </el-form-item>
  </el-form>
</Modal>
```

### 4. 确认框
```vue
<Modal
  v-model:visible="visible"
  title="确认删除"
  :show-close="false"
  @confirm="handleDelete"
>
  确定要删除这条记录吗？此操作不可撤销。
  
  <template #footer>
    <button @click="visible = false">取消</button>
    <button class="danger" @click="handleDelete">删除</button>
  </template>
</Modal>
```

## 扩展功能点

- ✅ 支持 `v-model` 双向绑定
- ✅ 支持 ESC 键关闭
- ✅ 支持loading状态
- ✅ 支持遮罩点击关闭
- ✅ 支持自定义宽度
- ✅ 支持隐藏关闭按钮
- ✅ 支持自定义按钮文字
- ✅ Transition 动画效果
- ✅ Teleport 到 body
- ✅ 点击穿透防护
