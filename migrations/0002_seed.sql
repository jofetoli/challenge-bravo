INSERT INTO public.currency(code, value, active, last_update)
    VALUES  
    ('USD','1.0', '1', '2021-01-15 17:17:49.629+02'),
    ('BRL','5.251', '1', '2021-01-15 17:17:49.629+02'),
    ('EUR','0.826712', '1', '2021-01-15 17:17:49.629+02'),
    ('BTC','0.000027724600453851707', '1', '2021-01-15 17:17:49.629+02'),
    ('ETH','0.0008609593670226734', '1', '2021-01-15 17:17:49.629+02');

INSERT INTO public.task_run(name, last_update)
    VALUES  
    ('CurrencyUpdate', '2021-01-15 17:17:49.629+02');

  