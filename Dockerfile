FROM quay.io/numigi/odoo-public:12.0
MAINTAINER numigi <contact@numigi.com>

USER odoo

COPY survey_type /mnt/extra-addons/survey_type
COPY survey_answer_for_partner /mnt/extra-addons/survey_answer_for_partner

COPY .docker_files/main /mnt/extra-addons/main
COPY .docker_files/odoo.conf /etc/odoo
