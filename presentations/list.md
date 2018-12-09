## Presentations
We make several presentations throughout the year during conferences and various events:

- Cruising Ocean Threat without Sinking Using TheHive, Cortex & MISP. [BSidesLisbon](https://bsideslisbon.org) 2018. November 29, 2018. ([PDF](TLP-WHITE-Bsides_Lisbon2018-TheHive_Cortex_MISP.pdf))
- TheHive & Cortex [UYBHYS](https://www.unlockyourbrain.bzh/) 2018. November 17, 2018. ( [PDF](TLP-WHITE-TheHive-Cortex_UYBHYS18.pdf))
- MISP, TheHive & Cortex: better, faster, happier. [MISP Summit](https://www.hack.lu/misp-summit/) 04. October 16, 2018.
([PDF](TLP-WHITE-TheHive-MISP_Summit_04v2.pdf))

## Workshops and Trainings
We frequently organize workshops and trainings, often with our friends from the [MISP Project](https://www.misp-project.org/). We do not publish all the materials because we often leverage MISP instances containing training-specific events and Cortex servers configured with commercial analyzers that supporting partners such as [DomainTools](https://www.domaintools.com/) and [Onyphe](https://www.onyphe.io/) kindly give us access to for the duration of the workshops and trainings.

If you'd like to attend a future workshop or training, please follow us on [https://twitter.com/thehive_project](Twitter) or regularly visit our [blog](https://blog.thehive-project.org). 

However, if you'd like to do the training at your own pace, you can find below the materials used for some of the workshops and trainings we gave in the past. Please note that you might have some difficulties completing the case studies without access to the commercial analyzers highlighted above.

### Botconf 2018
We gave a workshop during [Botconf](https://www.botconf.eu/) on Tue Dec 4, 2018. If you'd like to give it a try on your own, you will need:
- familiarity with TCP/IP, Linux (including editing configuration files), SSH & incident response
- the joint MISP, TheHive & Cortex [training VM](https://www.circl.lu/misp-training-images/thehive-misp.ova) ([SHA256 checksum](https://www.circl.lu/misp-training-images/checksums/packer_virtualbox-iso_virtualbox-iso_sha256.checksum))
- a powerful laptop with virtualization software (either VMware Workstation, VMware Fusion or VirtualBox)
- the ability to give the training VM 6GB of RAM and 2 processor cores. If that's not possible, we consider 4GB and 1 processor core the bare minimum
- the training [instructions](Botconf%202018/Instructions%20&%20Slides/Instructions.pdf) and [cheatsheet](Botconf%202018/Instructions%20&%20Slides/Cheatsheet.pdf)
- [Case Study 1](Botconf%202018/Case%20Studies/Case1-JoeSmith)
- [Case Study 2](Botconf%202018/Case%20Studies/Case2-AlertFeeder)

Before undertaking the workshop, we highly recommend reading the following slides in the specified order:
- [Threat Intelligence and Information Sharing with MISP](Botconf%202018/Instructions%20&%20Slides/TLP-WHITE-Botconf2018-MISP_CTI_Info_Sharing.pdf)
- [Detect, Investigate & Respond with MISP, TheHive & Cortex](Botconf%202018/Instructions%20&%20Slides/TLP-WHITE-Botconf2018-WS3-MISP_TheHive_Cortex.pdf)

**Important Note**: you won't be able to do case study 3 as it requires access to the instructors' MISP instance which is only available during the workshops and trainings. You must also skip the steps which ask you to synchronize your MISP instance with the instructors' (unless you have access to an instance pre-populated with events) or configure TheHive to leverage the instructors' Cortex instance.