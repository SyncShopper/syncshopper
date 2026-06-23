package com.syncshopper.dto.request;

import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.Map;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
@Schema(description = "Generic user event create request")
public class UserEventCreateRequest {

    @NotBlank(message = "Event type is required.")
    @Schema(description = "Event type", example = "AFFILIATE_CLICK", requiredMode = Schema.RequiredMode.REQUIRED)
    private String eventType;

    @Schema(description = "Product ID", example = "10")
    private Long productId;

    @Schema(description = "Recommendation ID", example = "15")
    private Long recommendationId;

    @NotBlank(message = "Source page is required.")
    @Schema(description = "Page where the event occurred", example = "EXTENSION_RESULT_PANEL", requiredMode = Schema.RequiredMode.REQUIRED)
    private String sourcePage;

    @Schema(description = "Video ID", example = "abc123")
    private String videoId;

    @Schema(description = "Category name", example = "Sneakers")
    private String categoryName;

    @Schema(description = "Brand name", example = "Nike")
    private String brand;

    @Schema(description = "Event target URL", example = "https://shopping.naver.com/product/123456789")
    private String targetUrl;

    @Schema(description = "Additional event metadata")
    private Map<String, Object> metadataJson;
}
