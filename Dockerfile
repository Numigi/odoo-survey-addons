FROM quay.io/numigi/odoo-public:14.8
MAINTAINER numigi <contact@numigi.com>

USER odoo

COPY survey_answer_for_partner /mnt/extra-addons/survey_answer_for_partner
COPY survey_condition /mnt/extra-addons/survey_condition
COPY survey_type /mnt/extra-addons/survey_type

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
