select distinct
    c.customer_id, -- id клиента
    c.gender, -- пол
    c.autopay_card, -- номер банковской карты
    c.email, -- адрес электронной почты
    c.msisdn, -- номер телефона
    c.region, -- регион
    i.activation_date, -- дата активации тарифа
    p2.allowance_voice, -- количество минут, включенных в тариф
    p2.allowance_sms, -- количество смс, включенных в тариф
    p2.allowance_data, -- количество Мб, включенных в тариф
    (select date_part('year',age(c.date_of_birth::date))) as age, -- возраст клиента
    (
	select sum(call_count)
	from raw.costed_event
	where
	    c.msisdn = raw.costed_event.calling_msisdn
	    and raw.costed_event.date::date >= date_trunc('day',current_timestamp - interval '1 month')
	    and raw.costed_event.date::date < date_trunc('day',current_timestamp)
    ) as sumcall, -- количество потраченных минут
    current_timestamp as execution_timestamp – текущая дата и время
from raw.customer as c
join raw.payments as p
    on c.customer_id = p.customer_id
join raw.instance as i
    on c.customer_id = i.customer_id
join raw.product as p2
    on i.product_id = p2.product_id
join raw.costed_event as c2
    on i.product_instance_id = c2.product_instance_id
where
    c.agree_for_promo = 'Yes' – согласие на рекламные рассылки
    and c.status = 'active' – статус клиента 'активный'
    and customer_category = 'phyzical' -- продвижение тарифа для группы людей 'физические лица'
    and i.status = 'active' – статус тарифа 'активный'
order by c.customer_id