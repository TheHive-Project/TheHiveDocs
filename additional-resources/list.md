# Additional Resources
The following page lists additional resources that should help you get more acquainted with TheHive, Cortex & other tools.

## Table of Contents
  * [Presentations](#presentations)
  * [Workshops and Trainings](#workshops-and-trainings)
    * [Hack\.lu 2019](#hacklu-2019)
    * [Botconf 2018](#botconf-2018)
  * [User Contributions](#user-contributions)

## Presentations
We make several presentations throughout the year during conferences and various events. Please find below some of the latest presentation material we produced:

- Cruising Ocean Threat without Sinking Using TheHive, Cortex & MISP. [BSidesLisbon](https://bsideslisbon.org) 2018. November 29, 2018. ([PDF](TLP-WHITE-Bsides_Lisbon2018-TheHive_Cortex_MISP.pdf))
- TheHive & Cortex [UYBHYS](https://www.unlockyourbrain.bzh/) 2018. November 17, 2018. ( [PDF](TLP-WHITE-TheHive-Cortex_UYBHYS18.pdf))
- MISP, TheHive & Cortex: better, faster, happier. [MISP Summit](https://www.hack.lu/misp-summit/) 04. October 16, 2018.
([PDF](TLP-WHITE-TheHive-MISP_Summit_04v2.pdf))

## Workshops and Trainings
We frequently organize workshops and trainings, often with our friends from the [MISP Project](https://www.misp-project.org/). We do not publish all the materials because we often leverage MISP instances containing training-specific events and Cortex servers configured with commercial analyzers that supporting partners such as [DomainTools](https://www.domaintools.com/) and [Onyphe](https://www.onyphe.io/) kindly give us access to for the duration of the workshops and trainings.

If you'd like to attend a future workshop or training, please follow us on [https://twitter.com/thehive_project](Twitter) or regularly visit our [blog](https://blog.thehive-project.org). 

However, if you'd like to do the training at your own pace, you can find below the materials used for some of the workshops and trainings we gave in the past. Please note that you might have some difficulties completing the case studies without access to the commercial analyzers highlighted above.

### Hack.lu 2019
We gave a workshop during [Hack.lu](https://2019.hack.lu) on Thu Oct 24, 2019. We prepared a MISP and Cortex instance on the cloud as well as a custom built training VM containing TheHive 3.4.0 which took advantage of those cloud instances.The VM was shared with the attendees during the workshop but will not be posted online. Indeed, the above-mentioned cloud instances were turned off after the workshop.

That being said, you can still get a look at the [slides](TLP-WHITE-Hack_lu2019-TheHive_Cortex_Workshop-v1.pdf) we used to set the stage for the workshop. They contain some valuable information if you are considering installing TheHive, Cortex & MISP or just beginning with the trio.

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

## User Contributions
The resources below have been contributed by our user community. Please note that the fact that they are listed here does not mean that they have been checked, validated or endorsed in any way by TheHive Project. Use your own judgment if you decide to read them.

- [TheHive Scripting: Task Imports](https://medium.com/@bromiley/thehive-scripting-task-imports-91a38480fac9), Matt B. Last accessed on March 26, 2019.
