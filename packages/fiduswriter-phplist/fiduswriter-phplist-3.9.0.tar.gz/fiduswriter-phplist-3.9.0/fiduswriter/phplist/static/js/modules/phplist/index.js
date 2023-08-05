import {post, addAlert, deactivateWait} from "../common"

import {formQuestion} from "./templates"

export class ConfirmAccountPHPList {
    constructor({page}) {
        this.confirmAccount = page
    }

    init() {
        this.addToForm()
    }

    addToForm() {
        this.confirmAccount.confirmQuestionsTemplates.push(formQuestion)
        this.confirmAccount.formChecks.push(
            () => document.querySelector('input[name=emaillist]:checked')
        )
        this.confirmAccount.confirmMethods.push(
            () => {
                const emailListRadio = document.querySelector('input[name=emaillist]:checked')
                if (!emailListRadio || emailListRadio.value === 'no') {
                    return
                }
                const email = this.confirmAccount.email
                return post(
                    '/proxy/phplist/subscribe_email',
                    {email}
                ).then(
                    () => {
                        deactivateWait()
                        if (emailListRadio) {
                            addAlert('info', gettext('Subscribed to email list'))
                        }
                        // Wait while message is shown
                        return new Promise(resolve => setTimeout(() => resolve(), 3000))
                    }
                ).catch(
                    error => console.error(error)
                )
            }
        )
    }


}
