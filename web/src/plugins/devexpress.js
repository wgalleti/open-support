import Vue from 'vue'
import 'devextreme/dist/css/dx.common.css'
import '@/assets/theme.css'
import 'devextreme/dist/js/localization/dx.messages.pt'
import ptMessage from 'devextreme/localization/messages/pt'
import { locale, loadMessages } from 'devextreme/localization'

import { DxTextArea } from 'devextreme-vue'

Vue.component(DxTextArea)

loadMessages(ptMessage)
locale('pt')
