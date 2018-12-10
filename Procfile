uwsgi : nohup uwsgi --socket 127.0.0.1:8000 -w runserver:app &
flask_sockets local : gunicorn -w 4 -b 127.0.0.1:8000 -k flask_sockets.worker --reload runserver:app

server0 : gunicorn --worker-class eventlet -w 1 runserver:app -u root -g apache --threads 4 --keep-alive 10
server1 : gunicorn --worker-class eventlet -w 1 -b 127.0.0.1:8001 runserver:app -u root -g apache --threads 4 --keep-alive 10
dev : gunicorn --worker-class eventlet -w 1 -b 127.0.0.1:9001 runserver:app -u root -g apache --threads 4 --keep-alive 10

flask_sockets remote :nohup gunicorn -w 4 -b 0.0.0.0:8000 -k flask_sockets.worker --reload runserver:app -u root -g apache &


SELECT username, created_at FROM users
     WHERE UPPER(username) IN
     (SELECT UPPER(username) FROM users GROUP BY UPPER(username) HAVING COUNT(*) > 1)
 ORDER BY username, created_at

 SELECT count(*) FROM users
      WHERE UPPER(username) IN
      (SELECT UPPER(username) FROM users GROUP BY UPPER(username) HAVING COUNT(*) > 1);

 trigger for inserting into user_notifications for each auction participants base on auction_notifications

CREATE OR REPLACE FUNCTION user_notification_inserter()
  RETURNS trigger AS
$BODY$
BEGIN
declare
  temprow record;
  BEGIN
    FOR temprow IN
            SELECT user_id FROM user_auction_participations WHERE user_auction_participations.auction_id=NEW.auction_id
        LOOP
            INSERT INTO user_auction_notifications(user_id,auction_notification_id,delivered,seen,created_at,updated_at) VALUES (temprow.user_id,NEW.id,false,false,now(),now());
        END LOOP;
  END;
 RETURN NEW;
END;
$BODY$
LANGUAGE plpgsql VOLATILE
COST 100;

CREATE TRIGGER save_user_notifications
  AFTER INSERT
  ON auction_notifications
  FOR EACH ROW
  EXECUTE PROCEDURE user_notification_inserter();

  CREATE OR REPLACE FUNCTION user_notification_updater()
    RETURNS trigger AS
  $BODY$
  BEGIN
  declare
    temprow record;
    BEGIN
      FOR temprow IN
              SELECT user_id FROM user_auction_participations WHERE user_auction_participations.auction_id=NEW.auction_id
          LOOP
              DELETE FROM user_auction_notifications WHERE user_id = temprow.user_id;
              INSERT INTO user_auction_notifications(user_id,auction_notification_id,delivered,seen,created_at,updated_at) VALUES (temprow.user_id,NEW.id,false,false,now(),now());
          END LOOP;
    END;
   RETURN NEW;
  END;
  $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

  CREATE TRIGGER refresh_user_notifications
    AFTER UPDATE
    ON auction_notifications
    FOR EACH ROW
    EXECUTE PROCEDURE user_notification_updater();

  CREATE OR REPLACE FUNCTION user_notification_remover()
    RETURNS trigger AS
  $BODY$
  BEGIN
  declare
    temprow record;
    BEGIN
      FOR temprow IN
              SELECT user_id FROM user_auction_participations WHERE user_auction_participations.auction_id=OLD.auction_id
          LOOP
              DELETE FROM user_auction_notifications WHERE user_id = temprow.user_id;
          END LOOP;
    END;
   RETURN NEW;
  END;
  $BODY$
  LANGUAGE plpgsql VOLATILE
  COST 100;

  CREATE TRIGGER remove_user_notifications
    AFTER DELETE
    ON auction_notifications
    FOR EACH ROW
    EXECUTE PROCEDURE user_notification_remover();


  // cascade

alter table user_auction_notifications
drop constraint user_auction_notifications_auction_notification_id_fkey,
add constraint user_auction_notifications_auction_notification_id_fkey
   foreign key (auction_notification_id)
   references auction_notifications(id)
   on delete set null;


    alter table user_notifications
    drop constraint user_notifications_user_id_fkey,
    add constraint user_notifications_user_id_fkey
       foreign key (user_id)
       references users(id)
       on delete set null;

user_notifications_notification_id_fkey

ALTER SEQUENCE auction_notifications_id_seq RESTART WITH 10000
