<?php
/**
 * Plugin Name: emulvent Machine Data
 * Description: Verwaltung von Maschinenmodellen + REST-API für Produktkonfigurator
 * Version: 1.0.0
 * Author: emulvent®
 * Author URI: https://emulvent.de
 * License: GPL v2 or later
 */

if ( ! defined( 'ABSPATH' ) ) {
    exit;
}

// ========================================
// 1. CUSTOM POST TYPE REGISTRIEREN
// ========================================

function emulvent_register_machine_post_type() {
    register_post_type(
        'machine_model',
        array(
            'labels'        => array(
                'name'          => 'Maschinenmodelle',
                'singular_name' => 'Modell',
                'all_items'     => 'Alle Modelle',
                'add_new_item'  => 'Neues Modell',
            ),
            'public'        => false,
            'show_in_rest'  => true,
            'rest_base'     => 'machine-models',
            'supports'      => array( 'title', 'editor', 'custom-fields' ),
            'taxonomies'    => array( 'machine_manufacturer' ),
            'show_in_menu'  => true,
            'capability_type' => 'post',
        )
    );
}
add_action( 'init', 'emulvent_register_machine_post_type', 10 );

// ========================================
// 2. CUSTOM TAXONOMY REGISTRIEREN
// ========================================

function emulvent_register_manufacturer_taxonomy() {
    register_taxonomy(
        'machine_manufacturer',
        'machine_model',
        array(
            'labels'           => array(
                'name'          => 'Hersteller',
                'singular_name' => 'Hersteller',
            ),
            'show_in_rest'     => true,
            'hierarchical'     => true,
            'publicly_queryable' => false,
        )
    );
}
add_action( 'init', 'emulvent_register_manufacturer_taxonomy', 10 );

// ========================================
// 3. META FIELDS REGISTRIEREN (REST API)
// ========================================

function emulvent_register_meta_fields() {
    $meta_fields = array(
        'container_volume_liters' => array( 'type' => 'number', 'label' => 'Behältervolumen (Liter)' ),
        'container_height_mm'     => array( 'type' => 'number', 'label' => 'Bauhöhe (mm)' ),
        'container_depth_mm'      => array( 'type' => 'number', 'label' => 'Bautiefe (mm)' ),
        'container_width_mm'      => array( 'type' => 'number', 'label' => 'Baubreite (mm)' ),
        'separator_count'         => array( 'type' => 'integer', 'label' => 'Anzahl Trennwände' ),
        'kss_water_mixed'         => array( 'type' => 'boolean', 'label' => 'Wassermischbar' ),
        'data_source'             => array( 'type' => 'string', 'label' => 'Datenquelle' ),
        'last_scraped_at'         => array( 'type' => 'string', 'label' => 'Zuletzt gescraped' ),
        'verification_count'      => array( 'type' => 'integer', 'label' => 'Validierungen' ),
    );

    foreach ( $meta_fields as $field => $config ) {
        register_rest_field(
            'machine_model',
            $field,
            array(
                'get_callback' => function( $post ) use ( $field ) {
                    return get_post_meta( $post['id'], $field, true );
                },
                'update_callback' => function( $value, $post ) use ( $field ) {
                    return update_post_meta( $post->ID, $field, $value );
                },
                'schema' => array(
                    'type'        => $config['type'],
                    'description' => $config['label'],
                )
            )
        );
    }
}
add_action( 'rest_api_init', 'emulvent_register_meta_fields', 10 );

// ========================================
// 4. REST-API ENDPOINT: ALLE MODELLE
// ========================================

function emulvent_get_all_machines_callback( $request ) {
    $args = array(
        'post_type'      => 'machine_model',
        'posts_per_page' => -1,
        'orderby'        => array( 'meta_value' => 'DESC', 'title' => 'ASC' ),
        'meta_key'       => 'last_scraped_at',
    );

    $posts = get_posts( $args );
    $models = array();

    foreach ( $posts as $post ) {
        $terms = wp_get_post_terms( $post->ID, 'machine_manufacturer', array( 'fields' => 'names' ) );
        $manufacturer = ! empty( $terms ) ? $terms[0] : 'Unknown';

        $models[] = array(
            'id'                      => $post->ID,
            'title'                   => $post->post_title,
            'manufacturer'            => $manufacturer,
            'container_volume_liters' => (int) get_post_meta( $post->ID, 'container_volume_liters', true ),
            'container_height_mm'     => (int) get_post_meta( $post->ID, 'container_height_mm', true ),
            'container_depth_mm'      => (int) get_post_meta( $post->ID, 'container_depth_mm', true ),
            'container_width_mm'      => (int) get_post_meta( $post->ID, 'container_width_mm', true ),
            'separator_count'         => (int) get_post_meta( $post->ID, 'separator_count', true ),
            'kss_water_mixed'         => (bool) get_post_meta( $post->ID, 'kss_water_mixed', true ),
            'data_source'             => get_post_meta( $post->ID, 'data_source', true ),
            'last_scraped_at'         => get_post_meta( $post->ID, 'last_scraped_at', true ),
            'verification_count'      => (int) get_post_meta( $post->ID, 'verification_count', true ),
        );
    }

    return new WP_REST_Response( $models, 200 );
}

register_rest_route(
    'machine-data/v1',
    '/models',
    array(
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'emulvent_get_all_machines_callback',
        'permission_callback' => '__return_true',
    )
);

// ========================================
// 5. SCRAPER-STATUS ENDPOINT (Admin only)
// ========================================

function emulvent_get_scraper_status_callback( $request ) {
    if ( ! current_user_can( 'manage_options' ) ) {
        return new WP_Error( 'rest_forbidden', 'Insufficient permissions', array( 'status' => 403 ) );
    }

    $status = get_option( 'emulvent_scraper_status', array() );
    return new WP_REST_Response( $status, 200 );
}

register_rest_route(
    'machine-data/v1',
    '/scraper-status',
    array(
        'methods'             => WP_REST_Server::READABLE,
        'callback'            => 'emulvent_get_scraper_status_callback',
        'permission_callback' => '__return_true',
    )
);

// ========================================
// 6. WEBHOOK: Status aktualisieren (für Scraper)
// ========================================

function emulvent_update_scraper_status_callback( $request ) {
    $auth_header = $request->get_header( 'Authorization' );
    $stored_token = get_option( 'emulvent_scraper_webhook_token' );

    if ( ! $auth_header || ! $stored_token ) {
        return new WP_Error( 'rest_unauthorized', 'Missing token', array( 'status' => 401 ) );
    }

    $provided_token = str_replace( 'Bearer ', '', $auth_header );

    if ( ! hash_equals( $stored_token, $provided_token ) ) {
        return new WP_Error( 'rest_unauthorized', 'Invalid token', array( 'status' => 401 ) );
    }

    $body = $request->get_json_params();
    update_option( 'emulvent_scraper_status', $body );

    return new WP_REST_Response( array( 'success' => true, 'message' => 'Status updated' ), 200 );
}

register_rest_route(
    'machine-data/v1',
    '/update-scraper-status',
    array(
        'methods'             => WP_REST_Server::CREATABLE,
        'callback'            => 'emulvent_update_scraper_status_callback',
        'permission_callback' => '__return_true',
    )
);

// ========================================
// 7. PLUGIN AKTIVIERUNG: TOKEN GENERIEREN
// ========================================

function emulvent_activate_plugin() {
    if ( ! get_option( 'emulvent_scraper_webhook_token' ) ) {
        $token = bin2hex( random_bytes( 32 ) );
        update_option( 'emulvent_scraper_webhook_token', $token );
    }

    if ( ! get_option( 'emulvent_plugin_version' ) || get_option( 'emulvent_plugin_version' ) !== '1.0.0' ) {
        update_option( 'emulvent_plugin_version', '1.0.0' );
    }
}
register_activation_hook( __FILE__, 'emulvent_activate_plugin' );

// ========================================
// 8. ADMIN-SEITE: TOKEN ANZEIGEN
// ========================================

function emulvent_add_admin_menu() {
    add_submenu_page(
        'edit.php?post_type=machine_model',
        'Scraper-Setup',
        'Scraper-Setup',
        'manage_options',
        'emulvent-scraper-setup',
        'emulvent_render_scraper_setup_page'
    );
}
add_action( 'admin_menu', 'emulvent_add_admin_menu' );

function emulvent_render_scraper_setup_page() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return;
    }

    $token = get_option( 'emulvent_scraper_webhook_token' );
    $status = get_option( 'emulvent_scraper_status', array() );
    $rest_url = get_rest_url( null, 'machine-data/v1' );

    ?>
    <div style="max-width: 900px; margin: 20px auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
        <h1>⚙️ emulvent® Scraper-Setup</h1>

        <div style="background: #f0f4f8; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>🔑 Webhook-Token (für GitHub Actions)</h2>
            <p>Kopiere diesen Token in GitHub Secrets als <code>WP_WEBHOOK_TOKEN</code>:</p>
            <code style="background: white; padding: 10px 15px; display: block; border: 1px solid #ddd; border-radius: 4px; font-family: 'Courier New', monospace; word-break: break-all; margin: 10px 0;">
                <?php echo esc_html( $token ); ?>
            </code>
            <button onclick="navigator.clipboard.writeText('<?php echo esc_attr( $token ); ?>'); alert('Token kopiert!');" style="padding: 8px 16px; background: #265887; color: white; border: none; border-radius: 4px; cursor: pointer;">
                📋 In Zwischenablage kopieren
            </button>
        </div>

        <div style="background: #f0f4f8; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>🔌 API-Endpunkte</h2>
            <ul>
                <li><strong>Alle Modelle abrufen:</strong><br>
                    <code style="background: white; padding: 8px 12px; display: inline-block; font-family: 'Courier New', monospace; border-radius: 4px; margin: 5px 0;">
                        GET <?php echo esc_url( $rest_url . '/models' ); ?>
                    </code>
                </li>
                <li><strong>Scraper-Status abrufen:</strong><br>
                    <code style="background: white; padding: 8px 12px; display: inline-block; font-family: 'Courier New', monospace; border-radius: 4px; margin: 5px 0;">
                        GET <?php echo esc_url( $rest_url . '/scraper-status' ); ?>
                    </code>
                </li>
                <li><strong>Status aktualisieren:</strong><br>
                    <code style="background: white; padding: 8px 12px; display: inline-block; font-family: 'Courier New', monospace; border-radius: 4px; margin: 5px 0;">
                        POST <?php echo esc_url( $rest_url . '/update-scraper-status' ); ?>
                    </code>
                </li>
            </ul>
        </div>

        <div style="background: #f0f4f8; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>📊 Aktueller Scraper-Status</h2>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; border-radius: 4px; overflow-x: auto;">
<?php echo esc_html( json_encode( $status, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) ); ?>
            </pre>
        </div>

        <div style="background: #e8f5e9; padding: 20px; border-radius: 8px; margin: 20px 0;">
            <h2>✅ Test-Anleitung</h2>
            <ol>
                <li>Diesen Token kopieren (Button oben)</li>
                <li>Terminal öffnen und ausführen:
                    <pre style="background: white; padding: 10px; border-radius: 4px; overflow-x: auto; font-family: 'Courier New', monospace; margin: 10px 0;">
curl https://emulvent.de/wp-json/machine-data/v1/models
                    </pre>
                </li>
                <li>Sollte <code>[]</code> zurückgeben (leeres Array, bis erste Daten gescraped werden)</li>
            </ol>
        </div>
    </div>
    <?php
}

// ========================================
// 9. DASHBOARD-SEITE ALS SHORTCODE
// ========================================

function emulvent_monitoring_dashboard_shortcode() {
    if ( ! current_user_can( 'manage_options' ) ) {
        return '<p style="color: red; font-weight: bold;">Zugriff verweigert. Nur für Administratoren.</p>';
    }

    $status = get_option( 'emulvent_scraper_status', array() );

    $args = array(
        'post_type'      => 'machine_model',
        'posts_per_page' => -1,
    );
    $all_posts = get_posts( $args );

    $manufacturers = array( 'DMG MORI', 'HAAS', 'GROB' );
    $model_counts = array();

    foreach ( $manufacturers as $mfr ) {
        $count = 0;
        foreach ( $all_posts as $post ) {
            $terms = wp_get_post_terms( $post->ID, 'machine_manufacturer', array( 'fields' => 'names' ) );
            if ( ! empty( $terms ) && $terms[0] === $mfr ) {
                $count++;
            }
        }
        $model_counts[ $mfr ] = $count;
    }

    ob_start();
    ?>
    <div style="max-width: 1000px; margin: 20px auto; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f9f9f9; padding: 30px; border-radius: 10px;">

        <h1 style="color: #265887; margin: 0 0 10px 0;">📊 emulvent® Machine Data Dashboard</h1>
        <p style="color: #666; margin: 0 0 30px 0;">Scraper-Status & Datenqualität (Live-Update)</p>

        <table style="width: 100%; border-collapse: collapse; background: white; border: 1px solid #ddd; border-radius: 6px; overflow: hidden;">
            <thead>
                <tr style="background: #265887; color: white;">
                    <th style="padding: 15px; text-align: left; font-weight: 600;">Hersteller</th>
                    <th style="padding: 15px; text-align: center; font-weight: 600;">Modelle</th>
                    <th style="padding: 15px; text-align: center; font-weight: 600;">Status</th>
                    <th style="padding: 15px; text-align: left; font-weight: 600;">Letzter Run</th>
                    <th style="padding: 15px; text-align: left; font-weight: 600;">Fehler</th>
                </tr>
            </thead>
            <tbody>
                <?php
                foreach ( $manufacturers as $mfr ) {
                    $mfr_status = $status[ strtolower( str_replace( ' ', '_', $mfr ) ) ] ?? array();
                    $count = $model_counts[ $mfr ] ?? 0;

                    $success = $mfr_status['success'] ?? false;
                    $status_icon = $success ? '✅ Success' : '⚠️ Pending';
                    $status_color = $success ? '#2ecc71' : '#f39c12';
                    $last_run = $mfr_status['last_run_at'] ?? '—';
                    $error = $mfr_status['error'] ?? '—';

                    echo sprintf(
                        '<tr style="border-bottom: 1px solid #eee;"><td style="padding: 15px;">%s</td><td style="padding: 15px; text-align: center; font-weight: 600;">%d</td><td style="padding: 15px; text-align: center; color: %s;">%s</td><td style="padding: 15px; font-family: monospace; font-size: 12px;">%s</td><td style="padding: 15px; font-family: monospace; font-size: 12px; color: #d32f2f;">%s</td></tr>',
                        htmlspecialchars( $mfr ),
                        $count,
                        $status_color,
                        $status_icon,
                        htmlspecialchars( $last_run ),
                        htmlspecialchars( $error )
                    );
                }
                ?>
            </tbody>
        </table>

        <div style="background: white; padding: 20px; margin: 20px 0; border-radius: 6px; border: 1px solid #ddd;">
            <h3 style="color: #265887; margin-top: 0;">📈 Zusammenfassung</h3>
            <p>
                <strong>Gesamtmodelle in DB:</strong> <?php echo count( $all_posts ); ?> <br>
                <strong>Letzte globale Aktualisierung:</strong> <code><?php echo esc_html( $status['last_global_run_at'] ?? 'Noch nie' ); ?></code> <br>
                <strong>API-Endpunkt:</strong> <code><?php echo esc_url( get_rest_url( null, 'machine-data/v1/models' ) ); ?></code>
            </p>
        </div>

        <div style="background: #f5f5f5; padding: 20px; border-radius: 6px; border: 1px solid #ddd;">
            <h3 style="color: #265887; margin-top: 0;">🔧 Debug-Info (JSON)</h3>
            <pre style="background: white; padding: 15px; border: 1px solid #ddd; border-radius: 4px; overflow-x: auto; font-family: 'Courier New', monospace; font-size: 12px;">
<?php echo esc_html( json_encode( $status, JSON_PRETTY_PRINT | JSON_UNESCAPED_SLASHES ) ); ?>
            </pre>
        </div>

    </div>
    <?php
    return ob_get_clean();
}
add_shortcode( 'emulvent_dashboard', 'emulvent_monitoring_dashboard_shortcode' );

?>
