<template>
    <div class="container">
        <el-card class="box-card" style="height: 500px; width: 600px;">
        <!-- 第一行，高度较高的信息显示区，有边框 -->
        <div class="info-box" style="height: 150px">
            <!-- 根据开关状态显示不同的信息 -->
            <div v-if="!isPoweredOn">
                NULL
            </div>
            <div v-else>
                <!-- 第一行 -->
                <el-row class="info-row">
                <el-col :span="12">
                    <div class="info-label">当前模式：</div>
                    <div class="info-value">{{ currentTemperature }}</div>
                </el-col>
                </el-row>
    
                <!-- 第二行 -->
                <el-row class="info-row">
                <el-col :span="12">
                    <div class="info-label">当前费率：</div>
                    <div class="info-value">{{ currentWindSpeed }}</div>
                </el-col>
                </el-row>
    
                <!-- 第三行 -->
                <el-row class="info-row">
                    <el-col :span="12">
                    <div class="info-label">中央空调温度：</div>
                    <div class="info-value">{{ setTemperature }}</div>
                </el-col>
                </el-row>
            </div>
        </div>
    
        <!-- 第二行，一个开机/关机按钮 -->
        <div class="row">
            <el-button :class="buttonClass" @click="togglePower">{{ powerButtonLabel }}</el-button>
        </div>
    
        <!-- 第三、四行，表单和按钮 -->
        <!-- 第三行，一个短输入栏和提交按钮 -->
        <div class="row">
        <el-form ref="form2" :model="form2" inline>
            <el-form-item label="设置中央空调模式">
                <el-select v-model="form2.field2" placeholder="请选择" style="width: 200px;">
                    <el-option label="Low" value="Low"></el-option>
                    <el-option label="Medium" value="Medium"></el-option>
                    <el-option label="High" value="High"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('form2')">SET</el-button>
            </el-form-item>
        </el-form>
        </div>
    
        <div class="row">
            <el-form ref="form3" :model="form3" inline>
                <el-form-item label="设置中央空调温度">
                    <el-input v-model="form3.field3" style="width: 200px;">
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('form3')">SET</el-button>
                </el-form-item>
            </el-form>
        </div>

        <div class="row">
            <el-form ref="form4" :model="form4" inline>
                <el-form-item label="设置费率">
                    <el-input v-model="form4.field4" style="width: 200px;">
                    </el-input>
                </el-form-item>
                <el-form-item>
                    <el-button type="primary" @click="submitForm('form4')">SET</el-button>
                </el-form-item>
            </el-form>
        </div>
        </el-card>
    </div>
</template>
    
<script>
    export default {
    data() {
        return {
            form2: {
                field2: ''
            },
            form3: {
                field3: ''
            },
            form4: {
                field4: ''
            },
    
            // 开关机按钮的状态
            isPoweredOn: false,
            currentTemperature: null,
            setTemperature: null,
            currentWindSpeed: null,
            setWindSpeed: null,
            airConditioningCost: null,
        };
    },
    computed: {
        // 计算属性，用于动态更新按钮文本
        buttonClass() {
            return this.isPoweredOn ? 'button-on' : 'button-off';
        },
        powerButtonLabel() {
            return this.isPoweredOn ? '关机' : '开机';
        }
    },
    methods: {
        togglePower() {
            // 切换开关机状态
            this.isPoweredOn = !this.isPoweredOn;
            console.log(this.isPoweredOn ? "开机" : "关机");
            // 如果开机，则请求空调信息
            if (this.isPoweredOn) {
                this.fetchAirConditioningInfo();
            }
        },
        fetchAirConditioningInfo() {
            // 这里是请求后端获取空调信息的逻辑
            // 假设您从后端获取的信息是一个对象，例如：
            // { currentTemperature: 24, setTemperature: 26, currentWindSpeed: 3, setWindSpeed: 2, airConditioningCost: 100 }
            // 您需要根据实际情况调整这个方法来适应您的后端接口
    
            // 模拟异步请求获取数据
            setTimeout(() => {
                this.currentTemperature = 24;
                this.setTemperature = 26;
                this.currentWindSpeed = 3;
                this.setWindSpeed = 2;
                this.airConditioningCost = 100;
            }, 1000);
        },
    }
    };
</script>

<style scoped>
.container {
display: flex;
justify-content: center; /* 水平居中 */
align-items: center; /* 垂直居中 */
height: 100vh; /* 全视口高度 */
}

.box-card {
width: 33%; /* 卡片宽度设置为页面的三分之一 */
}

.info-box {
border: 1px solid #dcdfe6; /* 信息区边框 */
padding: 10px;
margin-bottom: 20px;
flex-direction: column;
}

.row {
margin-bottom: 20px;
}

/* 添加自定义样式 */
.button-on {
    background-color: #f85050;
}
.button-off {
    /* 默认样式，可以根据需要进行调整 */
}

.info-row {
    margin-bottom: 10px; /* 行间距 */
}

.info-label, .info-value {
    display: inline-block; /* 内联块布局 */
}

.info-label {
    margin-right: 10px; /* 标签后的间隔 */
}
</style>
